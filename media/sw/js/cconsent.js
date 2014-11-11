;(function($) {
	var cc = {
		target: null,
		settings: {
			ignoreDoNotTrack: false,
			version: 1,
			expires: 365,
			txtInfo: 'Cookies are used',
			txtApprove: 'Approve',
			txtDecline: 'Decline',
			txtShow: 'Show',
			txtTypes: 'Types',
			txtPolicy: 'policy',
			needRestart: false,
			consent: null, // callback call to apply consent
			decline: null // callback called to apply decline
		},
		types: {
				'essential': {
					title: 'Essential cookies',
					desc: '',
					base: true
				},
				'social': {
					title: 'social',
					desc: '',
					base: false
				},
				'analytics': {
					title: 'analytics',
					desc: '',
					base: false
				}
		},
		 get_cookie: function (c_name) {
	        var i, x, y, ARRcookies = document.cookie.split(";");
	        for (i = 0; i < ARRcookies.length; i++) {
	            x = ARRcookies[i].substr(0, ARRcookies[i].indexOf("="));
	            y = ARRcookies[i].substr(ARRcookies[i].indexOf("=") + 1);
	            x = x.replace(/^\s+|\s+$/g, "");
	            if (x == c_name) {
	                return unescape(y);
	            }
	        }
			return false;
	    },
	    set_cookie: function (name, value, expirydays) {
	        var exdate = new Date();
	        exdate.setDate(exdate.getDate() + expirydays);
	        document.cookie = name + '=' + value + '; expires=' + exdate.toUTCString() + '; path=/'
	    },
	    delete_cookie: function (key) {
	        date = new Date();
	        date.setDate(date.getDate() - 1);
	        document.cookie = escape("cc_" + key) + '=; path=/; expires=' + date;
	    },
		check_donottrack: function(){
			cc.checkeddonottrack = true;
			if (!cc.settings.ignoreDoNotTrack) {
				if (navigator.doNotTrack == "yes" || navigator.doNotTrack == "1" || navigator.msDoNotTrack == "yes" || navigator.msDoNotTrack == "1") {
					cc.settings.dontnottrack  = true;
				} else {
					cc.settings.dontnottrack  = false;
				}
			}
		},		
		check_approval: function() {
			var response = cc.get_cookie('cc_response');
			if(response !== false) {
				cc.hide_banner();
				// now run response
				callback = null;
				if(response == 'consent') {
					if(cc.settings.consent) {
						var types = cc.get_cookie('cc_types');
						types = types.split(',');
						cc.settings.consent(types);
					}
				} else {
					if(cc.settings.decline) {
						cc.settings.decline.call();
					}
				}
				return;
			}
			cc.show_banner();
		},
		run: function(conf) {
			cc.target = $(conf.target),
			cc.settings = $.extend(cc.settings, conf.settings);
			cc.types = $.extend(cc.types, conf.types);
			cc.check_donottrack();
			cc.check_approval();			
		},
		onReset: function() {
			cc.delete_cookie('response');
			cc.delete_cookie('types');
			if (cc.settings.needRestart) {
				document.location.reload();
			}
			else {
				cc.check_approval();
			}
		},
		onConsent: function() {
			cc.set_cookie('cc_response', 'consent', cc.settings.expires);
			var conf = cc.settings, tt = [];
			for(var name in cc.types) {
				var type = cc.types[name];
				if( type.base) {
					continue;
				}
				var v = $('#cc-'+name).is(':checked');
				if(v) {
					tt.push(name);
				}
			}
			tt = tt.join(',');
			cc.set_cookie('cc_types', tt, cc.settings.expires);
			cc.hide_banner();
			if(conf.consent) {
				conf.consent.call();
			}
			if(conf.needRestart) {
				document.location.reload();
			}
		},
		onDecline: function() {
			var conf = cc.settings;
			cc.set_cookie('cc_response', 'decline', cc.settings.expires);
			cc.delete_cookie('types');
			cc.hide_banner();
			if(conf.decline) {
				conf.decline.call();
			}
			if(conf.needRestart) {
				document.location.reload();
			}
		},
		show_banner: function() {
			var conf = cc.settings, b = '<dl>', checked, old;
			for(var name in cc.types) {
				var t = cc.types[name];
				old = cc.get_cookie()
				b += '<dt>';
				if(t.base) {
					b += "&nbsp;&nbsp;&nbsp;"
				} else {
					checked = true;
					if(conf.dontnottrack) {
						checked = false;
					}
					if(old !== false) {
						checked = old_state;
					}
					checked = checked ? 'checked="checked"' : '';
					b += '<input type="checkbox" id="cc-'+name+'" '+checked+'/>';
				}
				b += '<label for="cc-'+name+'">'+t.title+'</label></dt><dd>'+t.desc+'</dd>';
			}
			b += '</dl>';
			html = '<div id="cc-banner"><span class="cc-info">'+conf.txtInfo+'</span><div id="cc-actions"><button id="cc-show">'+conf.txtShow+'</button> <button id="cc-consent">'+conf.txtApprove+'</button> <button id="cc-decline">'+conf.txtDecline+'</button></div><div id="cc-policy">'+conf.txtPolicy+'</div></div><div id="cc-types" style="display:none"><p>'+conf.txtTypes+'</p>'+b+'</div>';
			cc.target.html(html);
			$('body').addClass('cc-showed');
			$('#cc-show').click(function(){ 
				var $e = $('#cc-types');
				if( $e.is(':visible') ) {
					$e.slideUp();
				} else {
					$e.slideDown();	
				}
			});			
			$('#cc-consent').click(cc.onConsent);	
			$('#cc-decline').click(cc.onDecline);			
		},
		hide_banner: function() {
			cc.target.hide();
			$('body').removeClass('cc-showed');	
		}
	};
	$.cc = cc;
})(jQuery);
