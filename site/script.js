document.getElementById("discord_widget_id").onclick = function() {
	//alert('The client has not been released yet.');
	
	url = "discord-invite";
	window.open(
		url, "JarJar Client Discord", "height=400, width=600, modal=yes, alwaysRaised=yes"
	);
};


document.getElementById("download_link_id").onclick = function() {
	// alert('The client has not been released yet.');
	
	//download_url = "https://www.dropbox.com/s/ixyo2l5bodc5bwg/placeholder.txt?dl=0";
	// download_url = "https://en.wikipedia.org/wiki/Cheese";
	window.open(
		download_url, "JarJar Client Download", "height=800, width=600, modal=yes, alwaysRaised=yes"
	);
};
