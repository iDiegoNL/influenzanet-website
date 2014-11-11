var _gaq = _gaq || [];

/*
 * Google Analytics
 */
function start_ga() {
  var account = $('body').data('gga');
  _gaq.push(['_setAccount', account]);
  _gaq.push(['_setDomainName', 'none']);
  _gaq.push(['_setAllowLinker', true]);
  _gaq.push(['_trackPageview']);
 var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
 ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
 var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
};

/**
 * Social third parties
 */
function start_socials() {
 var html = '';
 html += '<iframe src="//platform.twitter.com/widgets/follow_button.html?screen_name=grippenet&lang=fr&show_count=false" allowtransparency="true" frameborder="0" scrolling="no" style="width:169px; height:21px;"></iframe>';
 html += '<iframe src="//www.facebook.com/plugins/like.php?href=https%3A%2F%2Fwww.facebook.com%2Fpages%2FGrippeNet%2F307427382625293&amp;send=false&amp;layout=button_count&amp;width=169&amp;show_faces=true&amp;action=like&amp;colorscheme=light&amp;font=verdana&amp;height=21" scrolling="no" frameborder="0" style="border:none; overflow:hidden; width:169px; height:21px;" allowTransparency="true"></iframe>';
 html += '<div class="addthis_toolbox addthis_default_style "><a class="addthis_button_preferred_1"></a><a class="addthis_button_preferred_2"></a><a class="addthis_button_preferred_3"></a>';
 html += '<a class="addthis_button_preferred_4"></a><a class="addthis_button_compact"></a><a class="addthis_counter addthis_bubble_style"></a></div>';
 html += '<script type="text/javascript" src="//s7.addthis.com/js/250/addthis_widget.js#pubid=xa-4f1e7fb169da798d"></script>';
 html += '</div>';
 $('#social-widgets').html(html);
}
