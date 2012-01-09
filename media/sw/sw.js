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
		url = $(this).attr('href');
		console.log('facebox');
		width = $(this).attr('data-facebox-width');
		height = $(this).attr('data-facebox-height');
		o = {};
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
		url = $(this).attr('href');
		console.log('facebox-iframe');
		width = $(this).attr('data-facebox-width');
		style = $(this).attr('data-iframe-style');
		opt = {};
		if(width) {
			opt.width = width;
		}
		show_facebox({iframe: {src: url, style: style}, top: 0 });
		return false;
	});
});

function show_facebox(options) {
	options = options || {};
	fb = $('#facebox');
	if(options.contents) {
		$('#facebox-content').html(options.contents);
	}
	if(options.iframe) {
		iframe = options.iframe;
		$('#facebox-content').html('<iframe src="'+iframe.src+'" style="'+iframe.style+'"></iframe>');
	}
	top = options.top ? options.top : 0;
	style = {top: options.top };
	if(options.width) {
		style.width = options.width;
	}
	if(options.height) {
		style.height = options.height;
	}
	fb.css(style);
	fb.overlay().load();
}
	