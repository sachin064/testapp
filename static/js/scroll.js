"use strict";
$(function($) {
	if($(window).width() > 767 )
	{
		var search_resultPageTop = $(".search-resultPage").offset().top;
		var nav_height = $("#header").height();
		var fiexd_div = $(".search-resultPage .fiexd-nav");
		if($(window).scrollTop() > search_resultPageTop - nav_height)
		{
			fiexd_div.addClass("fiexd");
		}
		else
		{
			fiexd_div.removeClass("fiexd");
		}
	}
	
	$(".fiexd-nav li a").each(function(){
		$(this).on('click',function(){ 
			$(".tab li").removeClass("active");
			$(this).parent().addClass("active");
			var click_id =  $(this).attr("href");
			
			var subs = click_id.indexOf("#");

			var count = 0;
			var index = $(this).index('.fiexd-nav li a');
			
			$(".tab-content").each(function(){
				if(count === index){
					var page_position = $(this).offset().top;
					var navbar_height = $(".fiexd-nav").height();
					if ($(window).width() > 767)
					{
						var target_position = page_position - navbar_height + 1 - 100;
					}
					else
					{
						var target_position = page_position - navbar_height + 1;
					}
					$("html,body").stop(true,true).animate({scrollTop:target_position + "px"},1000);							 		
				}
				count++;	
			});
			
		});
	});
});

$(window).on('scroll',function(){ 
	var search_resultPageTop = $(".search-resultPage").offset().top;
	var nav_height = $("#header").height();
	var fiexd_div = $(".search-resultPage .fiexd-nav");
	if($(window).scrollTop() > search_resultPageTop - nav_height)
	{
		fiexd_div.addClass("fiexd");
	}
	else
	{
		fiexd_div.removeClass("fiexd");
	}
	
	var windowPos = $(window).scrollTop(); // get the offset of the window from the top of page

	var page_position;
	var index = 0;
	var newindex = 0;
	windowPos = windowPos + 183;
	$(".tab-content").each(function(){
			page_position = $(this).offset().top;
			if(windowPos > page_position){
				newindex = $(this).index('.tab-content');
				if(newindex > index){
					index = $(this).index('.tab-content');
				}
			}		
	});
	index = index+1;
	$('.fiexd-nav li').removeClass("active");
	$('.fiexd-nav li:nth-child('+index+')').addClass("active");
});
$(window).on('resize',function(){
	$(window).trigger("scroll");
});