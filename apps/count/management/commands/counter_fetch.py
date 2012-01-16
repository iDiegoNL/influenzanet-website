from apps.count.sites import *
from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand
from optparse import make_option

class Command(BaseCommand):

    help = 'Fetch counter value'
    option_list = BaseCommand.option_list + (
        make_option('-c', '--country', action='store', type='string',
            dest='country', default='all',
            help='Country to fetch.'),
     )
     
    def handle(self, **options):
        
        country = options.get('country') 
        try:
            cache_delay = settings.COUNT_CACHE_TIMEOUT
        except AttributeError:
            cache_delay = 60 * 30

        if country == 'all':
            coutries = SOURCES.keys()
        else:
            coutries = [country]
        
        data = {}
        for c in coutries:
            result = site_fetch_count(c)
            data[c] = result
            # set in cache
            cache_key = "count-counter-%s" % c
            cache.set(cache_key, result, timeout=cache_delay)
            if(settings.DEBUG): 
                print("%s=%s " %(c, result))
        
            
  
