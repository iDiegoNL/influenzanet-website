from webassets import Bundle, Environment
from webassets.filter import Filter, register_filter
from django.conf import settings
from django.template import Template, Context
import os

env = Environment(directory=settings.MEDIA_ROOT, url=settings.MEDIA_URL)
env.debug = settings.DEBUG

def optional_file(file):
    """
    Include a file if exists, nothing if not
    """
    path = settings.MEDIA_ROOT
    if not path.endswith('/'):
        path += '/'
    path +=  file
    if os.path.exists(path):
        if env.debug:
            print "including %s" % path
        return file
    if env.debug:
        print "skipping %s" % path

    return Bundle()

class TemplateFilter(Filter):
    name = 'from_template'
    
    def output(self, _in, out, **kwargs):
        template = Template(_in.read())
        ctx = Context()
        out.write(template.render(ctx))

    def input(self, _in, out, **kwargs):
        out.write(_in.read())

register_filter(TemplateFilter)

###
# Common application Bundles
###

js_base = Bundle(
     'pollster/jquery/js/jquery-1.5.2.min.js',
     'sw/js/jquery-1.7.2.min.js',
     'pollster/jquery/js/jquery.tools.min.js',
     'sw/js/ui.jquerytools.js',
     'sw/js/mobile.js',
     Bundle('sw/js/thirdparties.js'), #, filters='yui_js'
     Bundle('sw/sw.js'), #, filters='yui_js'
     'sw/js/cconsent.js',
     'sw/js/cconsent.sw.js',
     output='assets/base.js'
  )

js_mailcheck = Bundle(
   'sw/js/mailcheck.min.js',
   optional_file('assets/domains.js'),
   output='assets/mailchecker.js'                   
) 
 
css_base = Bundle(
     'sw/css/_normalize.css',
     'sw/css/_base.css',                         
     'sw/css/layout.css',
     'sw/css/contents.css',
     'sw/css/menu.css',
     'sw/css/influenzanet.css',
     'sw/css/cconsent.css',
     'sw/css/survey.css',
     'sw/css/journal.css',
     'sw/css/widgets.css',
     'sw/css/facebox.css',
     'sw/css/feedback.css',
     'sw/css/avatars.css',
     'sw/css/users.css',
     'sw/css/user-group.css',
     'sw/css/tooltip.css',
     'sw/css/messages.css',
     'sw/css/cohort.css',
     output='assets/base.css',
     filters='cssrewrite,cssmin'
)
