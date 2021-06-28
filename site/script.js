document.getElementById("discord_widget_id").onclick = function() {
	url = "discord-invite";
	window.open(
		url, "JarJar Client Discord", "height=400, width=600, modal=yes, alwaysRaised=yes"
	);
};

document.getElementById("download_link_id").onclick = function() {
	alert("You need BETA for this! Enjoy some music instead?");

	url = "https://youtu.be/dQw4w9WgXcQ";
	window.open(
		url, "JarJar Download", "height=400, width=600, modal=yes, alwaysRaised=yes"
	);
};


// document.getElementById("download_link_id").onclick = function() {
// 	// alert("The client has not been released yet.");

// 	// download_url = "https://en.wikipedia.org/wiki/Cheese";
// 	window.open(
// 		download_url, "JarJar Client Download", "height=800, width=600, modal=yes, alwaysRaised=yes"
// 	);
// };
