/*!
* Start Bootstrap - Blog Home v5.0.2 (https://startbootstrap.com/template/blog-home)
* Copyright 2013-2021 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-blog-home/blob/master/LICENSE)
*/
// This file is intentionally blank

// Use this file to add JavaScript to your project

// Startup Scripts
$(document).ready(function()
{
	$('.hero').css('height', ($(window).height() - $('header').outerHeight()) + 'px'); // Set hero to fill page height

	$('#scroll-hero').click(function()
	{
		$('html,body').animate({scrollTop: $("#hero-bloc").height()}, 'slow');
	});
});


// Window resizes
$(window).resize(function()
{
	$('.hero').css('height', ($(window).height() - $('header').outerHeight()) + 'px'); // Refresh hero height
});