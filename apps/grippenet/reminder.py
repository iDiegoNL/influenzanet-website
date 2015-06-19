from django.conf import settings
from django.core.urlresolvers import reverse
from django.template import Context, loader
from django.contrib.sites.models import Site
from django.utils.translation import activate

import loginurl.utils
from apps.partnersites.context_processors import site_context

import datetime

def get_login_url(user, next):
    expires = datetime.datetime.now() + datetime.timedelta(days=30)

    usage_left = 5
    key = loginurl.utils.create(user, usage_left, expires, next)

    domain = Site.objects.get_current()
    path = reverse('loginurl-index').strip('/')
    loginurl_base = 'https://%s/%s' % (domain, path)

    return '%s/%s' % (loginurl_base, key.key)

def create_message(user, next=None):
    activate('fr')

    t = loader.get_template('pregnant.html')
    c = {
        'url': get_login_url(user, next),
    }
    c.update(site_context())
    
    site_url = 'https://%s' % Site.objects.get_current().domain
    media_url = '%s%s' % (site_url, settings.MEDIA_URL)
    
    c['site_url'] = site_url
    inner = t.render(Context(c))
    template = 'ggrippenet.html'
    t = loader.get_template(template)
    c['inner'] = inner
    c['MEDIA_URL'] = media_url
    return inner, t.render(Context(c))
