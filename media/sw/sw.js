/*!
 * GrippeNet.fr main <clement.turbelin@upmc.fr>
*/

// Declare console in case it is not available (IE..)
if(!window.console) {
	window.console = {
        log: function(e) { }
    };
}

$(function() {
	$('#counter').text( $('#count-fr').text() );
	if($.browser.msie) {
		var v = Math.ceil(parseFloat($.browser.version));
		v = 'ie'+ v;
		$('body').addClass('ie ' + v);
	}
	// Install facebox
	var mask = {
		zIndex: 1000,
		color: '#fff',
		loadSpeed: 200,
		opacity: 0.5
	};
	if($.browser.msie) {
		mask = 0; // disable expose mask on ie
	}
	if($.browser.mobile) {
		$.tools.overlay.conf.fixed = false;	
	}
	$('#facebox').overlay({top:'10%', mask: mask, closeOnClick: false});
	$.tools.tooltip.conf.tipClass = "hovertip";
	$.tools.tooltip.conf.layout = '<div><div class="tooltip-arrow"></div></div>';
	$.tools.tooltip.conf.offset = [-10, 0];
	initUI();
	var from = escape(document.location.pathname);
	$('#feedback-link').attr('href', '/feedback?from='+from);
	
});

function init_facebox_rel(ev) {
		var $e = $(this);
		var url = $e.attr('href'), width = $e.attr('data-facebox-width'), height = $e.attr('data-facebox-height');
		var o = {};
		if(width) {
			o.width = width;
		}
		if(height) {
			o.height = height;
		}
		if($.browser.mobile) {
			var $w = $(window);
			width = $w.width();
			height = $w.height();
		}
		if(url.indexOf('#') == 0) {
			o.contents = $(url).html();
			show_facebox(o);
		} else {
			$.ajax({
				url: url,
				success: function(data) {
					o.contents = data;
					show_facebox(o);
				}
			});	
		}
		return false;
}

function init_facebox_iframe(ev) {
	var $e = $(this);
	var url = $e.attr('href');
	var width = $e.attr('data-facebox-width');
	var style = $e.attr('data-iframe-style');
	var opt = {};
	if(width) {
		opt.width = width;
	}
	show_facebox({iframe: {src: url, style: style}, top: 0 });
	return false;
}

function initUI(container) {
	if(container) {
		container = container + ' ';
	} else {
		container = '';
	}
	console.log('initUI ' + container);
	$(container + 'a[rel=facebox]').click(init_facebox_rel);
	$(container +'a[rel=facebox-iframe]').click(init_facebox_iframe);
	$(container +'.tooltip').tooltip();
	$(container +'.tooltip-alert').tooltip({tipClass:'hovertip hovertip-alert'});
}

function show_facebox(options) {
	options = options || {};
	var fb = $('#facebox');
	if(options.contents) {
		$('#facebox-content').html(options.contents);
	}
	if(options.iframe) {
		var iframe = options.iframe;
		$('#facebox-content').html('<iframe src="'+iframe.src+'" style="'+iframe.style+'"></iframe>');
	}
	var top = 0;
	if(options.top) {
		top = options.top;
	}
	var style = {'top': top };
	if(options.width) {
		style.width = options.width;
	}
	if(options.height) {
		style.height = options.height;
	}
	fb.css(style);
	fb.overlay().load();
	var h = fb.height();
	$('#facebox-inner').height( h - 20 );
}

function close_facebox() {
	$('#facebox').overlay().close();
}

jQuery.fn.loading = function() {
	return $(this).html('<div class="loading"><img src="/media/sw/loader-2.gif" width="54" height="55"/></div>');
};
