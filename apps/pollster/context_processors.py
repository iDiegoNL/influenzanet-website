from apps import pollster

from apps.survey.views import _get_health_history

def last_survey(request):
    try:
        survey = pollster.models.Survey.get_by_shortname('weekly')
    except:
        return {}

    history = list(_get_health_history(request, survey))
    if not history:
        return {}

    return {
        'last_survey': history[0],
    }


def surveyuser_count(request):
    # not logged in, possibly other cases as well:
    if not hasattr(request, 'user') or not hasattr(request.user, 'surveyuser_set'):
        return {
            'surveyuser_count': 0,
            'surveyuser_gid': None,
        }

    surveyuser_qs = request.user.surveyuser_set.filter(deleted=False)
    return {
        'surveyuser_count': surveyuser_qs.count(),
        'surveyuser_gid': surveyuser_qs.get().global_id if surveyuser_qs.count() == 1 else None,
    }
