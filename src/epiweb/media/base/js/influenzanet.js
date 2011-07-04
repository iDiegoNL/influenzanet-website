/*
Template Name: Epiwork Main
Description: Javascript for deployment on the Epiwork platform 
Author: Antwan Wiersma (http://www.prime-creation.nl/)
Version: 1.0
*/

/* Google Analytics */

var _gaq = _gaq || [];
_gaq.push(['_setAccount', 'UA-24124829-1']);
_gaq.push(['_trackPageview']);

(function() {
  var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
  ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
  var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
})();

/* Influenzanet Map Bar */

var add_link = function() {
	$(this).next('div.toggle').attr('name', name);
	$(this).html('<a href="#top" title="Show/hide extra information">' +
	$(this).html() + '</a>');
};

var toggle = function() {
	$(this).
		toggleClass('expanded').
		nextAll('div.toggle').slideToggle('slow');
};

var remove_focus = function() {
	$(this).blur();
};

$(document).ready (function () {
	$('._toggle').
		removeClass('_toggle').
		addClass('toggle');	
	$('._expanded').
		removeClass('_expanded').
		addClass('expanded');
	$('._show').
		removeClass('_show').
		addClass('show');
	$('.jsclose').
		removeClass('jsclose').
		addClass('close');
	$('p.toggle:not(.expanded)').nextAll('div.toggle').hide();
	$('p.toggle').each(add_link);
	$('p.toggle').click(toggle);
	$('p.toggle a').mouseup(remove_focus);
});

$(function() {
	$('a.close').click(function(){
		$('div.toggle').slideToggle('slow');
		$('.expanded').
			removeClass('expanded').
			addClass('toggle');	
		return false;
	});
});

/* Open rel="external" links in a new window */

function externalLinks() {
 if (!document.getElementsByTagName) return;
 var anchors = document.getElementsByTagName("a");
 for (var i=0; i<anchors.length; i++) {
   var anchor = anchors[i];
   if (anchor.getAttribute("href") &&
       anchor.getAttribute("rel") == "external")
     anchor.target = "_blank";
 }
}
window.onload = externalLinks;

/* Mobily Map: Init */

$(function(){
	$('.europe_map').mobilymap({
		position: '0 344',
		popupClass: 'bubble',
		markerClass: 'point',
		popup: true,
		cookies: true,
		caption: true,
		setCenter: true,
		navigation: true,
		navSpeed: 3000,
		navBtnClass: 'navBtn',
		outsideButtons: '.map_buttons a',
		onMarkerClick: function(){},
		onPopupClose: function(){},
		onMapLoad: function(){}
	});
});

/* ==========================================================
 * MobilyMap
 * date: 29.11.2010
 * author: Marcin Dziewulski
 * last update: 20.1.2011
 * web: http://www.mobily.pl or http://playground.mobily.pl
 * email: hello@mobily.pl
 * Free to use under the MIT license.
 * ========================================================== */
(function($){$.fn.mobilymap=function(options){var defaults={position:"top left",popupClass:"bubble",markerClass:"point",popup:true,cookies:true,caption:true,setCenter:true,navigation:true,navSpeed:1000,navBtnClass:"navBtn",outsideButtons:false,onMarkerClick:function(){},onPopupClose:function(){},onMapLoad:function(){}};var sets=$.extend({},defaults,options);return this.each(function(){var $this=$(this);$this.css({position:"relative",overflow:"hidden",cursor:"move"});$this.wrapInner($("<div />").addClass("imgContent").css({zIndex:"1",position:"absolute"}));var content=$this.find(".imgContent"),image=$this.find("img"),title=image.attr("alt"),point=$this.find("."+sets.markerClass),mouseDown=false,mx,my,ex,ey,imgw=image.width(),imgh=image.height(),divw=$this.width(),divh=$this.height();var cookies={create:function(name,value,days){if(days){var date=new Date();date.setTime(date.getTime()+(days*24*60*60*1000));var expires="; expires="+date.toGMTString()}else{var expires=""}document.cookie=name+"="+value+expires+"; path=/"},erase:function(name){cookies.create(name,"",-1)},read:function(name){var nameEQ=name+"=";var ca=document.cookie.split(";");for(var i=0;i<ca.length;i++){var c=ca[i];while(c.charAt(0)==" "){c=c.substring(1,c.length)}if(c.indexOf(nameEQ)==0){return c.substring(nameEQ.length,c.length)}}return null}};var map={check:function(x,y){if(y<(divh-imgh)){y=divh-imgh}else{if(y>0){y=0}}if(x<(divw-imgw)){x=divw-imgw}else{if(x>0){x=0}}return{x:x,y:y}},init:function(position){map.preloader();switch(position){case"center":var x=(divw-imgw)/2,y=(divh-imgh)/2;break;case"top left":var x=0,y=0;break;case"top right":var x=divw-imgw,y=0;break;case"bottom left":var x=0,y=divh-imgh;break;case"bottom right":var x=divw-imgw,y=divh-imgh;break;default:var new_position=position.split(" "),x=-(new_position[0]),y=-(new_position[1]);if(y<(divh-imgh)){y=divh-imgh}else{if(y>0){y=0}}if(x<(divw-imgw)){x=divw-imgw}else{if(x>0){x=0}}}if(sets.cookies){if(cookies.read("position")!=null){var pos=cookies.read("position").split(","),x=pos[0],y=pos[1]}else{var x=(divw-imgw)/2,y=(divh-imgh)/2}}content.css({top:y+"px",left:x+"px"})},preloader:function(){var loadimg=new Image(),src=image.attr("src");image.css({visibility:"hidden"});$this.append($("<div />").addClass("loader").css({position:"absolute",zIndex:"10",top:"0",left:"0",width:"100%",height:"100%"}));$(loadimg).load(function(){image.css({visibility:"visible"});$this.find(".loader").fadeOut(1000,function(){$(this).remove();if(sets.caption){$this.append($("<div />").addClass("imgCaption").html(title).hide());captiond=$this.find(".imgCaption");captionh=captiond.innerHeight();captiond.css({bottom:-captionh+"px",position:"absolute",zIndex:"7"}).show().animate({bottom:0})}sets.onMapLoad.call(this)})}).attr("src",src);image.removeAttr("alt")},mouse:function(e){var x=e.pageX,y=e.pageY;return{x:x,y:y}},update:function(e){var mouse=map.mouse(e),x=mouse.x,y=mouse.y,movex=x-mx,movey=y-my,top=ey+movey,left=ex+movex,check=map.check(left,top);content.css({top:check.y+"px",left:check.x+"px"});if(sets.cookies){cookies.create("position",check.x+","+check.y,7)}},navigation:{buttons:function(){$this.prepend($("<div />").addClass("mapNav").css({position:"absolute",zIndex:"7",left:"20px",top:"20px"}));nav=$this.find(".mapNav");for(i=0;i<4;i++){nav.append('<a href="#" class="'+sets.navBtnClass+" "+sets.navBtnClass+i+'" rel="'+i+'">btn'+i+"</a>")}nav.bind({mouseenter:function(){if(sets.caption){captiond.stop()}}})},move:function(){$("."+sets.navBtnClass).bind({mousedown:function(){var navbtn=$(this).attr("rel");if(navbtn==0){content.animate({top:0},sets.navSpeed)}if(navbtn==1){content.animate({left:divw-imgw+"px"},sets.navSpeed)}if(navbtn==2){content.animate({top:divh-imgh+"px"},sets.navSpeed)}if(navbtn==3){content.animate({left:0},sets.navSpeed)}},mouseup:function(){content.stop();var pos=content.position(),x=pos.left,y=pos.top;if(sets.cookies){cookies.create("position",x+","+y,7)}},mouseout:function(){content.stop()},click:function(){return false}})}}};if(sets.navigation){map.navigation.buttons();map.navigation.move()}content.bind({mousedown:function(e){e.preventDefault();mouseDown=true;var mouse=map.mouse(e);mx=mouse.x,my=mouse.y;var element=content.position();ex=element.left,ey=element.top;map.update(e)},mousemove:function(e){if(mouseDown){map.update(e)}return false},mouseup:function(){if(mouseDown){mouseDown=false}return false},mouseout:function(){if(mouseDown){mouseDown=false}return false},mouseenter:function(){if(sets.caption){captiond.animate({bottom:-captionh+"px"})}return false},mouseleave:function(){if(sets.caption){captiond.animate({bottom:0})}return false}});map.init(sets.position);point.each(function(){var $this=$(this),pos=$this.attr("id").split("-");x=pos[1],y=pos[2];$this.css({position:"absolute",zIndex:"2",top:y+"px",left:x+"px"})}).wrapInner($("<div />").addClass("markerContent").css({display:"none"}));point.click(function(){var $this=$(this),pointw=$this.width(),pointh=$this.height(),pos=$this.position(),py=pos.top,px=pos.left,wrap=$this.find(".markerContent").html();if(sets.setCenter){var center_y=-py+divh/2-pointh/2,center_x=-px+divw/2-pointw/2,center=map.check(center_x,center_y);content.animate({top:center.y+"px",left:center.x+"px"})}if(sets.popup){$("."+sets.popupClass).remove();$this.after($("<div />").addClass(sets.popupClass).css({position:"absolute",zIndex:"3"}).html(wrap).append($("<a />").addClass("close")));var popup=$this.next("."+sets.popupClass),popupw=popup.innerWidth(),popuph=popup.innerHeight(),y=py,x=px;popup.css({top:y+pointh+"px",left:x+"px",marginLeft:-(popupw/2-pointw/2)+"px"})}else{sets.onMarkerClick.call(this)}return false});$this.find(".close").live("click",function(){var $this=$(this);$this.parents("."+sets.popupClass).remove();setTimeout(function(){sets.onPopupClose.call(this)},100);return false});if(sets.outsideButtons){$(sets.outsideButtons).click(function(){var $this=$(this),rel=$this.attr("rel");div=content.find("."+sets.markerClass).filter(function(){return $(this).attr("id")==rel});div.click();return false})}})}}(jQuery));

/* Register Jquery Widgets */

$(function(){

	// Accordion
	$("#accordion").accordion({ header: "h2", autoheight: false, active: true, alwaysOpen: false });

	// Tabs
	$('#tabs').tabs();
	
	//hover states on the static widgets
	$('#dialog_link, ul#icons li').hover(
		function() { $(this).addClass('ui-state-hover'); }, 
		function() { $(this).removeClass('ui-state-hover'); }
	);
	
});
