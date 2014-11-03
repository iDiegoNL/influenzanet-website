from django.conf import settings 

PROFILE_SURVEY = getattr(settings, 'POLLSTER_USER_PROFILE_SURVEY', 'intake')
