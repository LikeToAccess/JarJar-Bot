# -*- coding: utf-8 -*-
# filename          : bot.py
# description       : Discord bot interface for interacting with the website
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 06-24-2021
# version           : v1.0
# usage             : python bot.py
# notes             :
# license           : MIT
# py version        : 3.8.2 (must run on 3.6 or higher)
#==============================================================================
from datetime import date
from time import sleep
import os
import random
import discord
from discord.ext import commands#, tasks
from discord.errors import HTTPException
import markdown
import media


filenames = {
	"launcher_status": "launcher_status.txt",
	"credentials":     "credentials.md",
	"bad_words":       "bad_words.txt",
	"update_log":      "out.txt",
}
credentials = media.read_file(filenames["credentials"], filter=True)
token = credentials[0]
allowed_users = credentials[2:]
bot = commands.Bot(command_prefix=[
		"!",
	],
	help_command=None, case_insensitive=True)


@bot.event
async def on_ready():
	# check_logs.start()
	print(f"{bot.user} successfuly connected!")
	# await set_status("you for a fool! John McAfee payed his taxes!", discord.Status.online)
	await format_status(media.read_file(filenames["launcher_status"])[0])

@bot.event
async def on_message(msg):
	if msg.content.lower().startswith("ping"):
		await msg.channel.send("Pong!")
	elif ("bot" in msg.content.lower() or \
		"JarJar Bot" in msg.content.lower() or \
		"857809409959002132" in msg.content.lower()) and (
		"fucked" in msg.content.lower() or \
		"bad" in msg.content.lower() or \
		"dumb" in msg.content.lower()):
			await msg.author.send("Shud up, I'm the GREATEST bot!!!")
			await dm_profanity(msg.author)
	# print(msg)
	await bot.process_commands(msg)


# ADMIN ONLY COMMAND
@bot.command(name="status")
async def launcher_status(ctx, *args):
	if not await check_perms(ctx):
		return
	msg = " ".join(args)
	if len(args) == 1:
		msg = msg.upper()
	media.write_file(filenames["launcher_status"], msg)
	launcher = "online" if await format_status(msg) else "offline"
	await ctx.send(f"Status updated. Launcher {launcher}!")

# ADMIN ONLY COMMAND
@bot.command()
async def feed(ctx, *args):
	if not await check_perms(ctx):
		return
	start_break = "<!-- INJECT FEED START -->"
	end_break = "<!-- INJECT FEED END -->"
	filename = "site/index.html"
	avatar = get_author_avatar(ctx)
	author = ctx.author
	today = date.today()
	current_date = today.strftime("%B %d, %Y")
	msg = markdown.markdown(
		" ".join(args).replace("\\n", "<br>") \
		.replace("<script>","") \
		.replace("</script>","")
	)

	feed_content = f'''<div class="pad-left">\n<h4>({current_date})</h4>\n<a href="https://discord.com/users/{author.id}"><img src="{avatar}" alt="Disord user Avatar for {author.name}" align="left" width=45px height=45px class="icon">\n<div style="padding-left:55px">{author.name}</div>\n</a>\n<p style="padding-top:10px;">{msg}</p>\n</div>\n<hr class="solid">'''
	# await ctx.send(f"```html\n{feed_content}\n```")

	html_lines = media.read_file(filename)
	changed_lines = []
	for line in html_lines:
		if start_break in line:
			# line = line.split(start_break)[0]
			# line += f"{start_break}"
			line += f"\n{feed_content}\n"
			# line += f"\n{end_break}"
		changed_lines.append(line)
	media.write_file(filename, "\n".join(changed_lines))
	await ctx.send("New feed created.\nhttps://jarjar.tk/")

# PUBLIC COMMAND
@bot.command(name="help", description="Returns all commands available")
async def help_menu(ctx):
	help_text = "```"
	for command in bot.commands:
		if str(command) == "balls":
			command = "||MYSTERY COMMAND||"
		help_text+=f"\n{command}"
	help_text+="\n```"
	print(help_text)
	await ctx.send(help_text)

# PUBLIC COMMAND
@bot.command(aliases=["yaaminudes","nudes","sex","amogus"])
async def balls(ctx):
	await dm_profanity(ctx.author, sentance_length=5)

# PUBLIC COMMAND
@bot.command()
async def ping(ctx):
	await ctx.send("Pong!")

# ADMIN ONLY COMMAND
@bot.command()
async def find(ctx, *args):
	if not await check_perms(ctx, log_data=False):
		return
	# find <command [player] [count] | player [command] [count] | count>
	command = args[0].lower() if len(args) >= 1 else False
	player  = args[1].lower() if len(args) >= 2 else False
	count   = args[2]         if len(args) >= 3 else None
	commands_list = []
	for bot_command in bot.commands:
		commands_list.append(str(bot_command))

	# print(commands_list)
	if command not in commands_list:
		player, command = command, player
	if command:
		try:
			count = int(command)
			command = False
		except ValueError: count = False
	if player:
		try:
			count = int(player)
			player = False
		except ValueError: count = False
	# print(f"DEBUG: command={command}, player={player}, count={count}")

	resp = []
	log_data = media.read_file("log.txt", filter=True)[::-1]
	for line in log_data:
		line = line.replace("@", "(a)")
		if len(resp) >= int(count) and count:
			break
		if not player and command:
			if command in line.lower():
				resp.append(line)
		if player and command:
			if command in line.lower() and player in line.split("::")[0].split("]")[1].lower():
				resp.append(line)
		if player and not command:
			if player in line.split("::")[0].split("]")[1].lower():
				resp.append(line)
		if not player and not command:
			resp.append(line)

	target_length = 2000
	resp = "\n".join(resp)
	if len(resp) >= target_length:
		result = split_string(resp)
		while too_long(result):
			new_result = []
			for count, part in enumerate(result):
				halfed = split_string(part)
				new_result.append(halfed[0])
				new_result.append(halfed[1])
			result = new_result
	else:
		result = [resp]
	# print(result)

	print(f"DEBUG: command={command}, player={player}, count={count}")

	channel = bot.get_channel(857830007194517524)
	if ctx.channel.id != 857830007194517524:
		await ctx.send(f"Output redirected to {channel.name}")
	await channel.send(f"**Results of query with options, command={command}, player={player}, count={count}:**")
	try:
		for part in result:
			# print(part)
			# print(len(part))
			await channel.send(part)
	except HTTPException: await channel.send("Error, no results!")

# LIKETOACCESS ONLY COMMAND
@bot.command(name="authenticate", aliases=["auth", "trust"])
async def auth(ctx, user:discord.Member):
	if ctx.message.author.id == 354992856609325058:
		msg = f"\n# {user} ID\n{user.id}\n"  # TODO fix issues with non ASCII characters
		media.append_file("credentials.md", msg)
		await ctx.send(f"Added \"{user}\" to list of trusted admins")
		await media.log(ctx, True)
	else:
		await ctx.send("Only LikeToAccess can run this!")
		await media.log(ctx, False)

# ADMIN ONLY COMMAND
@bot.command()
async def update(ctx, *args):
	if not await check_perms(ctx, log_data=False):
		return
	filename = filenames["update_log"]
	media.remove_file(filename)
	try:
		os.system(f"update.cmd >> {filename}")
		sleep(5)
		await ctx.send("\n".join(media.read_file(filename)).split(".git")[1])
		os.system("start run.cmd")
		quit()
	except OSError as error:
		await ctx.send(f"Error:\n```{error}```")


async def dm_profanity(author=False, sentance_length=5):
	words = media.read_file(filenames["bad_words"])
	msg = " ".join([random.choice(words) for i in range(sentance_length)]).capitalize() + "."
	if author:
		await author.send(msg)
	return msg

# One-liner version LOL
# async def dm_profanity(author=False, sentance_length=5): return await author.send(msg) if author else " ".join([random.choice(media.read_file(filenames["bad_words"])) for i in range(sentance_length)]).capitalize() + "."

async def format_status(msg):
	if "down" in msg.lower() or "off" in msg.lower():
		launcher = False
		await set_status(
			activity=discord.Activity(type=discord.ActivityType.watching,
			name=f"Launcher-Status: {msg}"),
			status=discord.Status.do_not_disturb
		)
	else:
		launcher = True
		await set_status(
			activity=discord.Activity(type=discord.ActivityType.watching,
			name=f"Launcher-Status: {msg}"),
		)
	return launcher

async def set_status(activity, status=discord.Status.online):
	activity = discord.Game(activity) if isinstance(activity, str) else activity
	await bot.change_presence(status=status, activity=activity)

async def check_perms(ctx, log_data=True):
	global allowed_users
	allowed_users = media.read_file("credentials.md", filter=True)[2:]
	author = ctx.message.author
	if str(author.id) in allowed_users:
		if log_data: await media.log(ctx, True)
		return True
	if log_data: await media.log(ctx, False)
	return False

def get_author_avatar(ctx):
	author = ctx.author
	avatar = author.avatar_url
	return avatar

def split_string(string, seperator="\n"):
	print(len(string))
	string = string.split(seperator)
	resp = [seperator.join(string[:int(len(string)/2)]),seperator.join(string[int(len(string)/2):])]
	# print(resp)
	return resp

def too_long(data, target_length=2000):
	for item in data:
		if len(item) > target_length:
			return True
	return False

def run():
	return bot.run(token)


if __name__ == "__main__":
	run()
