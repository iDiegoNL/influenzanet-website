import os
import logging
from django.conf import settings
from webassets import Bundle, Environment
from webassets.loaders import PythonLoader
from webassets.script import CommandLineEnvironment

env = Environment('media/', 'media/')

env.debug = True

def optional_file(file, env):
        path = env.directory
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

# Base package

bundles = {
  'js:base': Bundle(
     'base/js/jquery-1.5.1.min.js',
     'base/js/influenzanet.js',
     'pollster/jquery/js/jquery.tools.min.js',
     'sw/sw.js',    
     output='assets/base.js'
  ),
 'js:pollster_run': Bundle(
    'pollster/wok/js/wok.pollster.js',
    'pollster/wok/js/wok.pollster.datatypes.js',
    'pollster/wok/js/wok.pollster.codeselect.js',
    'pollster/wok/js/wok.pollster.timeelapsed.js',
    'pollster/wok/js/wok.pollster.rules.js',
    'pollster/wok/js/wok.pollster.virtualoptions.js',
    'pollster/wok/js/wok.pollster.init.js',
    'pollster/wok/js/wok.pollster.lastyear.js',
  output='assets/pollster_run.js'
  ),
  'js:mailcheck': Bundle(
     'sw/js/mailcheck.min.js',
     optional_file('assets/domains.js', env),
     output='assets/mailchecker.js'                   
  )  
}

env.register(bundles)

#rewrite_url = get_filter('cssrewrite')


bundles_css = {
 'css:base':Bundle(
     'base/css/default.css',                         
     'sw/css/layout.css',
     'sw/css/survey.css',
     'sw/css/journal.css',
     'sw/css/widgets.css',
     'sw/css/facebox.css',
     'sw/css/feedback.css',
     'sw/css/users.css',
     'sw/css/tooltip.css',
     'sw/css/messages.css',
     'sw/css/cohort.css',
     output='assets/base.css',
     filters='cssrewrite,cssmin'
  )           
               
}

env.register(bundles_css)

log = logging.getLogger('webassets')
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

cmdenv = CommandLineEnvironment(env, log)
cmdenv.build()


