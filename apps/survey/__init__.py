from django.conf import settings

PROFILE_SURVEY = getattr(settings, 'POLLSTER_USER_PROFILE_SURVEY', 'intake')
WEEKLY_SURVEY = getattr(settings, 'POLLSTER_WEEKLY_SURVEY', 'weekly')

THANKS_WEEKLY_SURVEY  = 'dashboard_index'
THANKS_PROFILE_SURVEY = 'profile_thanks'