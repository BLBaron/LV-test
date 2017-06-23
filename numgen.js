//JavaScript for test code


(function() {
	'use strict'
	
	window.onload = function() {
		document.getElementById('start').onclick = displayStatus;
		document.getElementById('reading').style.display = "none";
		document.getElementById('stop').onclick = displayStatus2;
		
	}
	
	function displayStatus() {
		document.getElementById('waiting').style.display = "none";
		document.getElementById('reading').style.display = "block";
	}
	
	function displayStatus2() {
		document.getElementById('waiting').style.display = "block";
		document.getElementById('reading').style.display = "none";
	}
})();