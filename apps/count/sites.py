import urllib2

from apps.count.templatetags.count import SOURCES

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