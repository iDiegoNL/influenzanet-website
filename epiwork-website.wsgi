import os
import sys

path = '/var/www/influweb.it/httpdocs/epiwork-website'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

activate_this = '/var/www/influweb.it/httpdocs/epiwork-website/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
