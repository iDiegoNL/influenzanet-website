from optparse import make_option
from django.core.management.base import CommandError, BaseCommand
import os
from glob import glob
from fnmatch import fnmatch

from django.conf import settings


class Command(BaseCommand):
    help = 'Create the list of available avatars from the avatars directory'
    
    def handle(self, *args, **options):
        
        # Contains directory to avatars
        SURVEY_AVATARS = getattr(settings, 'SURVEY_AVATARS', None)
        
        if not settings.SURVEY_AVATARS:
            print "Avatars feature is not configured."
            print "SURVEY_AVATARS in settings should contain the name of the media's directory where avatars files are placed."
        
        path = settings.MEDIA_ROOT + '/' + SURVEY_AVATARS.strip('/')
        
        if not os.path.exists(path):
            raise Exception(path + " does not exist")
        
        cwd = os.getcwd()
        os.chdir(path)
        
        # Create the list from available images wich follow 
        # the convention : name is a number
        avatars = []
        for file in glob('*.png'):
            name = file.replace('.png','')
            if name.isdigit():
                avatars.append(str(name))
        
        # Create the config variable with list of available numbers
        if len(avatars):
            avatars = ','.join(avatars)
            code = "\nAVATARS = [%s]\n" % avatars
        else:
            code = "\nAVATARS = None\n"
        
        os.chdir(cwd)
        
        # Create the config variable with list of available numbers
        fn = 'apps/survey/avatars.py'
        f = open(fn,'w')
        f.write(code)
        print "Avatar list created in " + fn
