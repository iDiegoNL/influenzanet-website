"""
Functions to handle waiting message between online seasons
""" 

"""
Configuration in local_settings

SURVEY_WAIT_LAUNCH = True/False # Activate/deactivate the waiting page

SURVEY_WAIT_MESSAGE = {'content': 'My message', 'title': 'My title'}

SURVEY_LAUNCH_DATE = '2013-11-13' # Launch date to show (only before this date)
"""

from datetime import datetime, date
from django.conf import settings

WAIT_LAUNCH = getattr(settings,'SURVEY_WAIT_LAUNCH', False)

def is_wait_launch(request, survey=None):
    """
    Check if request need to be restricted in case of WAIT_LAUNCH context
    Returns True if platform should show a waiting message
    """
    if not WAIT_LAUNCH:
        return False
    if survey is not None:
        allowed_surveys = getattr(settings, 'SURVEY_WAIT_ALLOWED', None)
        if allowed_surveys:
            if survey in allowed_surveys:
                return False
    # Now check if one condition allow to pass by the waiting message 
    test_users = getattr(settings, 'SURVEY_TEST_USERS', None)
    if test_users:
        user_id = request.user.id
        if user_id in test_users:
            return False
    return True

def get_wait_launch_context(request):
    """ 
    Get the context of waiting message
    Used to render the wait_launch template
    """ 
    if is_wait_launch(request):
        if hasattr(settings, 'SURVEY_LAUNCH_DATE'):
            d = settings.SURVEY_LAUNCH_DATE
            if d:
                d = datetime.strptime(d,'%Y-%m-%d')
                d = d.date()
                if date.today() < d:
                    # Do not show launch date if it is in the past
                    d = None
        else:
            d = None
        if hasattr(settings, 'SURVEY_WAIT_MESSAGE'):
            message = settings.SURVEY_WAIT_MESSAGE
        else:
            message = False
        return {'date':  d, 'message': message }
    return None

def get_wait_launch_date():
    """
    Get the launch date if defined and if the season is not started
    """
    d = False
    if hasattr(settings, 'SURVEY_LAUNCH_DATE'):
        d = settings.SURVEY_LAUNCH_DATE
        if d:
            try:
                d = datetime.strptime(d,'%Y-%m-%d')
                d = d.date()
                if date.today() >= d:
                    d = False # dont show launch date after the date
            except:
                d = False
        else:
            d = False
    return d