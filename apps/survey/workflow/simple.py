'''
Created on 15 nov. 2017

@author: ClementTurbelin
'''
from apps.survey.workflow import SurveyWorkflow
from apps.survey import PROFILE_SURVEY, THANKS_PROFILE_SURVEY, THANKS_WEEKLY_SURVEY
from django.core.urlresolvers import reverse


class SimpleWorkflow(SurveyWorkflow):
    """
        Simple Workflow for extra survey
        Redirect to a dedicated thank page
    """
    def after_save(self, context):
        shortname = context.survey.shortname
        next_url = None
        if 'next' not in context.request.GET:
            if shortname == PROFILE_SURVEY:
                next_url = reverse(THANKS_PROFILE_SURVEY)
            elif shortname == "weekly":
                next_url = reverse(THANKS_WEEKLY_SURVEY)
            else:
                next_url = reverse('survey_run_thanks', kwargs={"shortname": shortname})
        else:
            next_url = context.request.GET['next']
        return next_url
