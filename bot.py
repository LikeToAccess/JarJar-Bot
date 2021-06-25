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
import discord
from discord.ext import commands#, tasks
from discord.errors import HTTPException
import markdown
import media


credentials = media.read_file("credentials.md", filter=True)
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
	await set_status("you for a fool! John McAfee payed his taxes!", discord.Status.online)

# ADMIN ONLY COMMAND
@bot.command(name="status")
async def launcher_status(ctx, *args):
	if not await check_perms(ctx):
		return
	if len(args) == 1:
		args = " ".join(args).upper()
	else:
		args = " ".join(args)
	if "down" in args.lower() or "off" in args.lower():
		launcher = False
		await set_status(
			activity=discord.Activity(type=discord.ActivityType.watching,
			name=f"Launcher-Status: {args}"),
			status=discord.Status.do_not_disturb
		)
	else:
		launcher = True
		await set_status(
			activity=discord.Activity(type=discord.ActivityType.watching,
			name=f"Launcher-Status: {args}"),
		)
	launcher = "online" if launcher else "offline"
	await ctx.send(f"Status updated. Launcher {launcher}!")

# ADMIN ONLY COMMAND
@bot.command()
async def feed(ctx, *args):
	if not await check_perms(ctx):
		return

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

	feed_content = f'''<h4>({current_date})</h4>\n<img src="{avatar}" alt="Disord user Avatar for {author.name}" align="left" width=45px height=45px style="padding-right:10px">\n<a href="https://discord.com/users/{author.id}">{author.name}</a>\n<p style="padding-top:10px;">{msg}</p>\n<hr class="solid">'''
	await ctx.send(f"```html\n{feed_content}\n```")

	html_lines = media.read_file(filename)
	changed_lines = []
	for line in html_lines:
		if end_break in line:
			line = line.split(end_break)[0]
			line += f"\n{feed_content}"
			line += f"\n{end_break}"
		changed_lines.append(line)
	media.write_file(filename, "\n".join(changed_lines))

# @bot.command(name="help", description="Returns all commands available")
# async def help(ctx):
#     helptext = "```"
#     for command in bot.commands:
#         helptext+=f"{command}\n"
#     helptext+="```"
#     print(helptext)
#     await ctx.send(helptext)


@bot.command()
async def find(ctx, *args):
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
		msg = f"\n# {user} ID\n{user.id}\n"
		media.append_file("credentials.md", msg)
		await ctx.send(f"Added \"{user}\" to list of trusted admins")
		await media.log(ctx, True)
	else:
		await ctx.send("Only LikeToAccess can run this!")
		await media.log(ctx, False)

# ADMIN ONLY COMMAND
@bot.command()
async def update(ctx):
	if not await check_perms(ctx):
		return
	filename = "out.txt"
	media.remove_file(filename)
	try:
		os.system(f"update.cmd >> {filename}")
		sleep(5)
		await ctx.send("\n".join(media.read_file(filename)).split(".git")[1])
		os.system("start run.cmd")
		quit()
	except OSError as error:
		await ctx.send(f"Error:\n```{error}```")



async def set_status(activity, status=discord.Status.online):
	activity = discord.Game(activity) if isinstance(activity, str) else activity
	await bot.change_presence(status=status, activity=activity)

async def check_perms(ctx):
	global allowed_users
	allowed_users = media.read_file("credentials.md", filter=True)[2:]
	author = ctx.message.author
	if str(author.id) in allowed_users:
		await media.log(ctx, True)
		return True
	await media.log(ctx, False)
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