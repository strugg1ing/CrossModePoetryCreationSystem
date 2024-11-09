jQuery(function(){
	"use strict";
		$(".navList .navLi").hover(function(){
		$(this).addClass("active");
		$(this).find(".navSub").stop().slideDown();	
	},function(){
		$(this).removeClass("active");
		$(this).find(".navSub").stop().slideUp();
		$(".navThrList").slideUp();
		$(".navFouList").slideUp();
	});
	function scro(){
			if($(document).scrollTop()>50){$(".headerbg").addClass("active");}else{$(".headerbg").removeClass("active");}
		}
		scro();
		$(window).scroll(function(){
			scro();
		});
			$(".benefits_name").hover(function(){
			$(this).addClass("hover");
			$(this).stop().animate({bottom: "0px", opacity:1 , height:"400px"}, "fast");
		},function(){
			$(this).removeClass("hover");
			$(this).stop().animate({bottom: "0px", opacity:1 , height:"400px"}, "fast") ; 			
		}
	);
		$(".Program_name ").hover(function() {
	    $(this).addClass("hover");
		$(this).find(".Program_title").stop()
		.animate({ opacity:1 , height:"100%"}, "fast")
		.css("display","block");

	}, function() {
	    $(this).removeClass("hover");  
		$(this).find(".Program_title").stop()
		.animate({ opacity: 1,height:"40px"}, "fast")
		.css("display","block");
	});
		$(".user_casestyle").hover(function(){
			$(this).addClass("hover");
			$(this).find(".hd a").css("display","block");
			//$(this).stop().animate({bottom: "0px", opacity:1 , height:""}, "fast")
		},function(){
			$(this).removeClass("hover");
			$(this).find(".hd a").css("display","none");
			//$(this).stop().animate({bottom: "0px", opacity:1 , height:""}, "fast")  			
		}
	);
	//置顶图标显示
$('#top-back').hide();
$(window).scroll(function(){
	 if($(this).scrollTop() > 350){
		$("#top-back").fadeIn();
	 }
	 else{
		$("#top-back").fadeOut();
	 }
  });
		$(".bannerN").css("background-image", "url(" + $(".bannerN").find("img").attr("src") + ")");
//置顶事件
function topBack(){
  $('body,html').animate({scrollTop:0},300);
}
var oWidth=$(".tips-box").width();
	$(".index-btn").click(function(){
		$(".tips-box").animate({
			left:50 +'%',
			marginLeft:-oWidth/2,
		},900);
		$(this).hide();
	});
	$(".tips-img").click(function(){
		$(".tips-box").animate({
			left:100 + '%',
			marginLeft:'',
		},900);
		$(".index-btn").show();
	});

});
$(document).ready(function(){
"use strict";
	
  var $backgrounds = $(".product_list").find(".parallax-bg"),
      LAYER_OFFSET = 30,
      PRLX_SPEED = 2500,
      $slider; 
  $slider = $("#slider").tlrkSlider({
    autoStart: true,
    animationStart: function(ev, slider, step){
      var max_steps = this.framesCount; 
      $backgrounds.each(function(idx, el){
        var pos = (step * (100 / max_steps)) + (LAYER_OFFSET * idx);
        $(this).animate({"backgroundPosition": pos + "% 0"}, PRLX_SPEED);
      });
    },
    elements: {
      "img": {delay: 10},
      "h2": {delay: 500},
      ".copy": {delay: 800},
      ".button": {delay: 1000}
    }
  });
  
  $(".product_list")
    .hover(
      function(){$(this).find(".slider-prev, .slider-next").show();},
      function(){$(this).find(".slider-prev, .slider-next").hide();}
    )
    .find(".slider-prev").click(function(){$slider.tlrkSlider("go", "prev"); return false; }).end()
    .find(".slider-next").click(function(){$slider.tlrkSlider("go", "next"); return false; });


// custom formatting example
$('#count-number').data('countToOptions', {
formatter: function (value, options) {
  return value.toFixed(options.decimals).replace(/\B(?=(?:\d{3})+(?!\d))/g, ',');
}
});

// start all the timers
$('.timer').each(count);  

function count(options) {
	var $this = $(this);
	options = $.extend({}, options || {}, $this.data('countToOptions') || {});
	$this.countTo(options);
}
});
$.fn.countTo = function (options) {
	"use strict";
	options = options || {};	
	return $(this).each(function () {
		// set options for current element
		var settings = $.extend({}, $.fn.countTo.defaults, {
			from:            $(this).data('from'),
			to:              $(this).data('to'),
			speed:           $(this).data('speed'),
			refreshInterval: $(this).data('refresh-interval'),
			decimals:        $(this).data('decimals')
		}, options);
		
		// how many times to update the value, and how much to increment the value on each update
		var loops = Math.ceil(settings.speed / settings.refreshInterval),
			increment = (settings.to - settings.from) / loops;
		
		// references & variables that will change with each update
		var self = this,
			$self = $(this),
			loopCount = 0,
			value = settings.from,
			data = $self.data('countTo') || {};
		
		$self.data('countTo', data);
		
		// if an existing interval can be found, clear it first
		if (data.interval) {
			clearInterval(data.interval);
		}
		data.interval = setInterval(updateTimer, settings.refreshInterval);
		
		// initialize the element with the starting value
		render(value);
		
		function updateTimer() {
			value += increment;
			loopCount++;
			
			render(value);
			
			if (typeof(settings.onUpdate) == 'function') {
				settings.onUpdate.call(self, value);
			}
			
			if (loopCount >= loops) {
				// remove the interval
				$self.removeData('countTo');
				clearInterval(data.interval);
				value = settings.to;
				
				if (typeof(settings.onComplete) == 'function') {
					settings.onComplete.call(self, value);
				}
			}
		}
		
		function render(value) {
			var formattedValue = settings.formatter.call(self, value, settings);
			$self.html(formattedValue);
		}
	});
};

$.fn.countTo.defaults = {
	from: 0,               // the number the element should start at
	to: 0,                 // the number the element should end at
	speed: 300,           // how long it should take to count between the target numbers
	refreshInterval: 100,  // how often the element should be updated
	decimals: 0,           // the number of decimal places to show
	formatter: formatter,  // handler for formatting the value before rendering
	onUpdate: null,        // callback method for every time the element is updated
	onComplete: null       // callback method for when the element finishes updating
};

function formatter(value, settings) {
	return value.toFixed(settings.decimals);
}
/*************伸缩************/
;(function($){
    $.fn.fix = function(options){
        var defaults = {
            float : 'left',
			menu:220,
			minStatue : false,
			skin : 'blue',
			durationTime : 1000	
        }
        var options = $.extend(defaults, options);		
        this.each(function(){			
            //获取对象
			var thisBox = $(this),
				closeBtn = thisBox.find('.close_btn' ),
				show_btn = thisBox.find('.show_btn' ),
				sideContent = thisBox.find('.side_content'),
				sideList = thisBox.find('.side_list'),
				sidetitle=thisBox.find('.side_title'),
				scrollsidebar=thisBox.find('.Tutorial_content');	
			    var defaultTop = thisBox.offset().top;	//对象的默认top	
			
			thisBox.css(options.float, 0);			
			if(options.minStatue){
				$(".show_btn").css("float", options.float);
				sideContent.css('width', 0);
				show_btn.css('width', 25);
			}
			scrollsidebar.css({"width":$(window).width()-(options.menu)});
			//当窗口发生改变是触发
			 $(window).resize(function(){	
			 scrollsidebar.css({"width":$(window).width()-(options.menu)});
			 });
			//close事件
			closeBtn.bind("click",function(){
				sideContent.animate({width: '0px'},"fast").addClass('active');
            	show_btn.stop(true, true).delay(300).animate({ width: '25px'},"fast");
				sideList.css("display","none");
				sidetitle.css("display","none");
				show_btn.css("display","block")
				scrollsidebar.addClass("Widescreen")
			});
			//show事件
			 show_btn.click(function() {
	            $(this).animate({width: '0px'},"fast").css('display','none');
	            sideContent.stop(true, true).delay(0).animate({ width: '220px'},"fast");
				sideList.css("display","block")
				sidetitle.css("display","block");
				scrollsidebar.removeClass("Widescreen");
				
	        });		
        });	//end this.each
    };
})(jQuery);
