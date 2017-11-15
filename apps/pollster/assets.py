from webassets import Bundle
import os.path as osp
import cms
from django.conf import settings
from apps.common.i18n import get_locale

js_pollster_run_base = Bundle(
    'pollster/wok/js/wok.pollster.js',
    'pollster/wok/js/wok.pollster.datatypes.js',
    'pollster/wok/js/wok.pollster.codeselect.js',
    'pollster/wok/js/wok.pollster.timeelapsed.js',
    'pollster/wok/js/wok.pollster.visualscale.js',
    'pollster/wok/js/wok.pollster.rules.js',
    'pollster/wok/js/wok.pollster.virtualoptions.js',
    output='assets/pollster_runbase.js' # not used
)

js_pollster_run = Bundle(
  js_pollster_run_base,
  'pollster/wok/js/wok.pollster.init_run.js',
  output='assets/pollster_run.js'
)

js_pollster_edit = Bundle(
  'pollster/jquery/js/jquery.hoverIntent.minified.js',
  js_pollster_run_base,
  'pollster/wok/js/wok.pollster.providers.js',
  'pollster/wok/js/wok.pollster.designer.js',
  'pollster/wok/js/wok.pollster.init_edit.js',
  output='assets/pollster_edit.js'
)

css_pollster_run = Bundle(
   'pollster/jquery/css/smoothness/jquery-ui-1.8.14.css',
   'pollster/css/survey.css',
   'pollster/css/skin.css',
   'sw/css/pollster.css',
  output='assets/pollster.css'
)

# Path to cms media files
cms_path = osp.dirname(cms.__file__)
cms_media = osp.join(cms_path, 'media')

js_pollster_base = Bundle(
  # 'pollster/jquery/js/jquery-1.5.2.min.js',
  'pollster/jquery/js/jquery-ui-1.8.14.min.js',
  'sw/js/jquery.ui.touch-punch.min.js',
  # 'pollster/jquery/js/jquery.tools.min.js',
  'pollster/jquery/js/jquery.form.js',
  'pollster/jquery/js/jquery.cookie.js',
  'pollster/wok/js/wok.jquery.js',
  'pollster/wok/js/wok.properties.js',
  osp.join(cms_media, 'cms/js/csrf.js'),
  output='assets/pollster_base.js'
)

for lng in settings.LANGUAGES:
    language = lng[0]
    locale = get_locale(language)
    globals()['js_pollster_date_' + language] = Bundle(
       'pollster/jquery/js/i18n/jquery.ui.datepicker-'+ language + '.js',
       'pollster/datejs/js/date-'+ locale +'.js',
       Bundle('sw/js/datejs.fr.js' ),
       output='assets/pollster_date_' + language +'.js'
    )



""""
    {% if locale_code %}
    <script type="text/javascript" src="/media/pollster/jquery/js/i18n/jquery.ui.datepicker-{{ language }}.js"></script>
    <script type="text/javascript" src="/media/pollster/datejs/js/date-{{ locale_code }}.js"></script>
    {% else %}
    <script type="text/javascript" src="/media/pollster/datejs/js/date.js"></script>
    {% endif %}

    <script type="text/javascript" src="{{ CMS_MEDIA_URL }}js/csrf.js"></script>
    <script type="text/javascript">jQuery().cmsPatchCSRF()</script>
    <script type="text/javascript" src="{% url pollster_urls %}"></script>
"""
