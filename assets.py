import settings
from django.template import Template
import re
import os.path
from functools import partial

try:
    import cssmin
    CSS_MINIFIER = True
except:
    CSS_MINIFIER = False

# bundle file definifions
# key = file relative path and name
# value = list of files to include
bundles_js = {
 'assets/base':(
     'base/js/jquery-1.5.1.min.js',
     'base/js/influenzanet.js',
     'pollster/jquery/js/jquery.tools.min.js',
     'sw/sw.js',    
  )           
           
}

bundles_css = {
 'assets/base':(
     'base/css/default.css',                         
     'sw/css/layout.css',
     'sw/css/survey.css',
     'sw/css/journal.css',
     'sw/css/widgets.css',
     'sw/css/facebox.css',
     'sw/css/feedback.css',
     'sw/css/users.css',
     'sw/css/tooltip.css',
  )           
}

BUNDLE_PATH = settings.MEDIA_ROOT + '/'

def change_path(m, path_to ):
 p = m.group(1)
 if(p == ''):
     return ''
 path = os.path.normpath(os.path.realpath(p))
 path = os.path.relpath(path, path_to)
 path = path.replace("\\",'/')
 return "url(%s)" % path
 
def process_file(filename, type, path_to, context=None):
    f = file(filename)
    contents = f.read()
    f.close()
    if type == 'css':
        fd = os.path.dirname(filename)
        old_cwd = os.getcwd()
        os.chdir(fd)
        path_to = os.path.normpath(path_to)
        rep = partial(change_path, path_to=path_to)
        contents = re.sub(r"url\((.*)\)", rep, contents) 
        os.chdir(old_cwd)
        
    if type == 'css' and CSS_MINIFIER:
        print '  = minify css'
        contents = cssmin.cssmin(contents)
    return contents
    
def compile_bundle(bundle, ext):
    if ext == 'js':
        comment = "// %s \n"
    else:
        comment = "/* %s  */\n"
        
    for name,list in bundle.items():
        print 'Bundle %s' % name
        contents = ''
        filename = BUNDLE_PATH + name + '.' + ext
        path_to = os.path.dirname(filename)
        for b in list:
            print ' + '+ b
            contents += "\n"
            contents += comment % b 
            b = settings.MEDIA_ROOT + '/' + b
            contents += process_file(b, ext, path_to)
            contents += "\n"
        f = file(filename,'w')
        f.write(contents)

# Main

if CSS_MINIFIER:
    print 'css minifier cssmin'
        
compile_bundle(bundles_js, 'js')
compile_bundle(bundles_css, 'css')