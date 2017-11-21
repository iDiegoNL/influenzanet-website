'''
Created on 21 nov. 2017

@author: ClementTurbelin
'''

from .models import PregnantCohort, ImmunoCohort
from .workflow import IMMUNO_COHORT_ID, PREGNANT_COHORT_ID, IMMUNO_CHANNEL, PREGNAT_CHANNEL
from apps.pollster.runner import WORKFLOWS

def get_cohort_users(persons):

        persons_ids = [p.id for p in persons]

        pregnants = list(PregnantCohort.objects.filter(survey_user__id__in=persons_ids))
        pregnants = dict([(str(p.survey_user.id), p) for p in pregnants])

        immuno = list(ImmunoCohort.objects.filter(survey_user__id__in=persons_ids))
        immuno = dict([(str(p.survey_user.id), p) for p in immuno])

        return {
            PREGNANT_COHORT_ID: pregnants,
            IMMUNO_COHORT_ID: immuno,
        }

def get_cohorts():
    cohorts  = {}
    for w in WORKFLOWS:
        if hasattr(w, 'get_cohort_id'):
            id = w.get_cohort_id()
            cohorts[id] = True
    return cohorts

def get_survey_user_channel(survey_user):
    cohorts = get_cohorts()
    channel = ''

    if cohorts.has_key(PREGNANT_COHORT_ID):
        pregnant = None
        try:
            pregnant = PregnantCohort.objects.get(survey_user=survey_user)
        except PregnantCohort.DoesNotExist:
            pass

        if pregnant is not None:
            if pregnant.change_channel:
                channel = PREGNAT_CHANNEL

    if channel != '':
        return channel

    if cohorts.has_key(IMMUNO_COHORT_ID):
        p = None
        try:
            p = ImmunoCohort.objects.get(survey_user=survey_user)
        except ImmunoCohort.DoesNotExist:
            pass

        if p is not None:
            if p.change_channel:
                channel = IMMUNO_CHANNEL

    return channel