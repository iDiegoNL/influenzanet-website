import os
import sys

path = '/home/bifi/apps/epiwork-website'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
