from optparse import make_option
from django.core.management.base import CommandError, BaseCommand
import os
from glob import glob
from fnmatch import fnmatch
class Command(BaseCommand):
    help = 'Create the list of available avatars from the media/avatar directory'
    
    def handle(self, *args, **options):
        
        path = 'media/avatars'
        
        if not os.path.exists(path):
            raise Exception(path + " does not exists")
        
        cwd = os.getcwd()
        os.chdir(path)
        
        avatars = []
        for file in glob('*.png'):
            name = file.replace('.png','')
            if name.isdigit():
                avatars.append(str(name))
        
        if len(avatars):
            avatars = ','.join(avatars)
            code = "\nAVATARS = [%s]\n" % avatars
        else:
            code = "\nAVATARS = None\n"
        
        os.chdir(cwd)
        
        f = open('apps/survey/avatars.py','w')
        f.write(code)
