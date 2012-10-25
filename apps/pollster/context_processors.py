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

    return {'last_survey': history[-1]}
