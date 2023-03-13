$(document).ready(function(){


	$('li').click(function(){

		var imgpath = $(this).attr('dir');

		$('#image').html('<img width="300" src='+imgpath+'>');

	});



});
