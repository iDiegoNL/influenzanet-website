import urllib2

from apps.count.templatetags.count import SOURCES
from django.contrib.auth.models import User

def fetch_accounts():
    return User.objects.filter(is_active=True).count()

def site_fetch_count(country):
    try:
        result = urllib2.urlopen(SOURCES[country], timeout=2).read()
    except Exception, e:
        print e
        result = 'NA'
    try:
        int(result)
    except ValueError:
        result = 'NA'

    return result    