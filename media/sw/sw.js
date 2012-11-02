if(!window.console) {
	window.console = {
        log: function(e) { }
    };
}

$(function() {
	$('#counter').text( $('#count-fr').text() );
	if($.browser.msie) {
		var v = Math.ceil(parseFloat($.browser.version));
		v = 'ie'+v;
		$('body').addClass('ie '+v);
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
	$('#facebox').overlay({ top: '10%', mask: mask, closeOnClick: false});
	$('a[rel=facebox]').click(function(ev){
		var url = $(this).attr('href');
		console.log('facebox');
		var width = $(this).attr('data-facebox-width');
		var height = $(this).attr('data-facebox-height');
		var o = {};
		if(width) {
			o.width = width;
		}
		if(height) {
			o.height = height;
		}
		$.ajax({
			url: url,
			success: function(data) {
				o.contents = data;
				show_facebox(o);
			}
		});
		return false;
	});
	$('a[rel=facebox-iframe]').click(function(ev){
		var url = $(this).attr('href');
		console.log('facebox-iframe');
		var width = $(this).attr('data-facebox-width');
		var style = $(this).attr('data-iframe-style');
		var opt = {};
		if(width) {
			opt.width = width;
		}
		show_facebox({iframe: {src: url, style: style}, top: 0 });
		return false;
	});
	
	$('.tip').tooltip();
	
	var from = escape(document.location.pathname);
	$('#feedback-link').attr('href', '/feedback?from='+from);
	
	
});

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