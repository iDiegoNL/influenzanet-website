from apps.count.sites import *
from django.conf import settings
from django.core.cache import cache
from django.core.management.base import NoArgsCommand, BaseCommand


class Command(NoArgsCommand):
  # fetch all sites
  data = dict([(country, site_fetch_count(country)) for country in SOURCES.keys() ])
  
  try:
      cache_delay = settings.COUNT_CACHE_TIMOUT
  except AttributeError:
   cache_delay = 60 * 30 
  
  for country in SOURCES.keys():
      key = "count-counter-%s" % country
      cache.set(key, data[country], timeout=cache_delay)

  cache.set("count-counter-all", data, timeout=cache_delay)
  
