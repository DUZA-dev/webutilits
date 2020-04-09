$(document).ready(function(){
	$('.content').height($(window).height()-$('.navbar').height());
});

$(window).resize(function(){
	 $('.content').height($(window).height()-$('.navbar').height());
});