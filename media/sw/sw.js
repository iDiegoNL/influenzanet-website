/*!
 * GrippeNet.fr main <clement.turbelin@upmc.fr>
*/

// Declare console in case it is not available (IE..)
if(!window.console) {
	window.console = {
        log: function(e) { }
    };
}

$.isOldIE = function() {
	return $('html').hasClass('lt-ie9');
};

$(function() {
	$('html').removeClass('no-js');
	if($.browser.msie) {
		var v = Math.ceil(parseFloat($.browser.version));
		v = 'ie'+ v;
		$('body').addClass('ie ' + v);
	}
	install_ui();
	initUI();
	var from = escape(document.location.pathname);
	$('#feedback-link').attr('href', '/feedback?from='+from);
	
});

jQuery.fn.loading = function() {
	return $(this).html('<div class="loading"><img src="/media/sw/loader-2.gif" width="54" height="55"/></div>');
};
