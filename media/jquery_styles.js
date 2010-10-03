jQuery(document).ready(function(){

//CDN FALLBACK
if (typeof jQuery == 'undefined') {
	document.write(unescape("%3Cscript src='http://code.jquery.com/jquery-1.4.2.min.js' type='text/javascript'%3E%3C/script%3E"));
}

/*
//NAV: HIGHLIGHT CURRENT PAGE'S TAB
var path = location.pathname.substring(1);
if (path == 'lists/'){
	$('nav #home').addClass('selected');
}
if (path == 'lists/create/'){
	$('nav #create').addClass('selected');
}

//NAV: SLIDE OUT
var navDuration = 300;
var navJumpHeight = "50px";

$('nav li').hover(
	function() {
		$(this).animate({ top: '-='+navJumpHeight }, navDuration);
	},
	function() {
		$(this).animate({ top: '+='+navJumpHeight }, navDuration);
	}
);
*/
});