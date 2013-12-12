#from optparse import make_option
from django.core.management.base import CommandError, BaseCommand
from getpass import getpass
from ...models import EpiworkUser
from optparse import make_option
from django.contrib.auth import authenticate
from django.db import transaction
from django.db import connection
from django.contrib.auth.models import User
import sys
import csv

from apps.accounts.provider import UserProvider

class Command(BaseCommand):
    help = 'Export actions'
    
    option_list = BaseCommand.option_list  + (
        make_option('-u', '--table', action='store', dest='table', default=None, help='User id in table'),
        make_option('-f', '--file', action='store', dest='file', default=None, help='Source id in file'),
        make_option('-w', '--what', action='store', dest='fields', default=None, help='Coma separated list of field to export'),
        make_option('-o', '--output', action='store', dest='output', default=None, help='Output file'),
    )

    def handle(self, *args, **options):
        
        # verbose = int(options['verbosity'])
        
        pwd = getpass("root django password : ")
        
        root = authenticate(username="root", password=pwd)
        
        if root is None:
            print "uh oh, wrong try"
            return
    
        # del args[0]
        print "Access granted"
        
        users = []
        if options['table']:
                query = "SELECT user_id FROM " + options['table']
                cursor = connection.cursor()
                cursor.execute(query)
                users = [ row[0] for row in cursor.fetchall()]
        
        export = []
        fields = ['email']
        for user in EpiworkUser.objects.filter(is_active=True):
            dju = user.get_django_user()
            if dju.id in users:
                d = {}
                for field in fields:
                    d[field] = getattr(user, field)
                export.append(d)
        
        if options['output'] is not None:
            f = open(options['output'],'wb')
        else:
            f = sys.stdout
        w = csv.DictWriter(f, fields, extrasaction='ignore')
        for row in export:
            w.writerows(export)
        if options['output'] is not None:
            f.close()
            