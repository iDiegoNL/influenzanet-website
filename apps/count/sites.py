import urllib2

from django.core.cache import cache 

SOURCES = {
    'nl': 'http://www.degrotegriepmeting.nl/count/counter/?country=NL',
    'be': 'http://www.degrotegriepmeting.nl/count/counter/?country=BE',
    'de': 'http://www.aktivgegengrippe.de/count/counter/',
    'at': 'http://www.aktivgegengrippe.at/count/counter/',
    'ch': 'http://www.aktivgegengrippe.ch/count/counter/',
    'se': 'http://www.influensakoll.se/count/counter/',
    'uk': 'http://flusurvey.org.uk/count/counter/',
    'it': 'http://www.influweb.it/count/counter/',
    'pt': 'http://www.gripenet.pt/count/counter/',
    'fr': 'http://www.grippenet.fr/count/counter/',
}

def site_fetch_count(country):
    try:
        result = urllib2.urlopen(SOURCES[country], timeout=2).read()
    except:
        result = '0'

    try:
        int(result)
    except ValueError:
        result = '0'

    return result    