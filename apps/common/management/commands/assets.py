import logging
import sys
from os import path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from webassets import  Environment, Bundle
from webassets.loaders import PythonLoader, LoaderError
from webassets.script import (CommandError as AssetCommandError,
                              GenericArgparseImplementation)

# Common build env is defined in assets module in the package
from apps.common.assets import env

def import_bundles(bundles, signatures, app):
    try:
        module_uri = app + '.assets'
        # print 'looking for ' + module_uri
        loader = PythonLoader(module_uri)
        #module = import_module(module_uri)
        print '> importing %s ' % module_uri
        try:
            # module_bundles = module.bundles
            module_bundles = loader.load_bundles()
        except:
            print '<no bundle found>'
            return
        for name, bundle in module_bundles.iteritems():
            if not isinstance(bundle, Bundle):
                continue
            signature = name + '@' + module_uri
            if signatures.has_key(signature):
                print "Bundle %s already included" % signature
                continue
            if bundles.has_key(name):
                print ' * merging ' + name
                ## merge into an existing module
                b = bundles[name]
                print b.contents
                b.contents = b.contents + (bundle,)
            else:
                print ' + adding ' + name
                bundles[name] = bundle
            signatures[signature] = 1 
            
    except LoaderError, e:
        pass
    
def show_bundle(bundle, indent=0):
    h = ' ' * indent 
    print '%s <output=%s, filters=%s>' % (h, bundle.output, bundle.filters,)
    for f in bundle.contents:
        if isinstance(f, basestring):
            print h + ' + ' + f
        else:
            show_bundle(f, indent + 2)

class Command(BaseCommand):

    help = 'Manage assets'
    args = 'build|show'
    requires_model_validation = False

    def handle(self, *args, **options):
        
        log = logging.getLogger('webassets')
        log.addHandler(logging.StreamHandler())
        log.setLevel(logging.DEBUG)
        
        try:
            command = args[0]
        except IndexError:
            print "subcommand build|show must be provided"
            return
        
        bundles = {}
        ## Search for app local assets bundles    
        ## If a bundle is defined with the same name as the global one
        ## Bundles are appened to the existing bundle    
        apps = []
        signatures = {}
        for app in settings.INSTALLED_APPS:
            if app in apps:
                print "*Caution* app %s is referenced several times" % app
                continue
            import_bundles(bundles, signatures, app)
            apps.append(app)
        
        if command == 'show':
            for name, bundle in bundles.iteritems():
                print '* package %s ' % name
                show_bundle(bundle, 2)
            return
        
        env.register(bundles)
        
        prog = "%s assets" % path.basename(sys.argv[0])
        impl = GenericArgparseImplementation(env=env, log=log, no_global_options=True, prog=prog)
        try:
            impl.run_with_argv(args)
        except AssetCommandError, e:
            raise CommandError(e)
        







        
            
  
