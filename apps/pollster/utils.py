from . import models
from django.conf import settings

# @todo: move this function from pollster to survey appp app 
# should not handle specific survey features

def get_user_profile(user_id, global_id):
    try:
        shortname = getattr(settings, 'POLLSTER_USER_PROFILE_SURVEY', 'intake')
        survey = models.Survey.get_by_shortname(shortname)
        survey.set_caching(getattr(settings, 'POLLSTER_USE_CACHE', False))
        profile = survey.get_last_participation_data(user_id, global_id)
        return profile
    except models.Survey.DoesNotExist:
        return None
    except StandardError, e:
        return None        