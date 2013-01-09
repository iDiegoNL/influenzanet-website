from __future__ import absolute_import

from django.template import Library
from django.core.cache import cache 
from ..sites import fetch_accounts
register = Library()

CACHE_KEY = 'active_accounts'

def active_accounts():
    nb = cache.get(CACHE_KEY)
    if not nb :
        nb = fetch_accounts()
        cache.set(CACHE_KEY, nb, timeout=60 * 30) 
    return nb

register.simple_tag(active_accounts)
