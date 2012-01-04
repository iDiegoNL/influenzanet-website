from apps.count.sites import *
from django.conf import settings
from django.core.cache import cache
from django.core.management.base import NoArgsCommand, BaseCommand


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
         
        try:
            cache_delay = settings.COUNT_CACHE_TIMOUT
        except AttributeError:
            cache_delay = 60 * 30

        data = {}
        for country in SOURCES.keys():
            result = site_fetch_count(country)
            data[country] = result
            # set in cache
            key = "count-counter-%s" % country
            cache.set(key, result, timeout=cache_delay)
            if(settings.DEBUG): 
                print("%s=%d " %(country,result))
        
        cache.set("count-counter-all", data, timeout=cache_delay)
  
