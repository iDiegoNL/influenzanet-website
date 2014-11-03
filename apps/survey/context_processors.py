from .household import SurveyHousehold

def household(request):
    # not logged in, possibly other cases as well:
    if not hasattr(request, 'user') or not hasattr(request.user, 'surveyuser_set'):
        return {
                'count': 0,
                'gid': None
                } 

    household = SurveyHousehold.get_household(request)
    count = household.count()
    gid = None
    if count == 1:
        gid = household.gids(0)
    return {
            'household_count': count,
            'household_gid' : gid,
            }
