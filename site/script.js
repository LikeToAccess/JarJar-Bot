document.getElementById("download_link_id").onclick = function() {
	alert('The client has not been released yet.');
	
	//download_url = "https://www.dropbox.com/s/ixyo2l5bodc5bwg/placeholder.txt?dl=0";
	download_url = "https://en.wikipedia.org/wiki/Cheese";
	window.open(
		download_url, "Azure Client Download", "height=400, width=600, modal=yes, alwaysRaised=yes"
	);
};
