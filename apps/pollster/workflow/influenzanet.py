##
# Default Workflow for influenzaNet
##
from apps.pollster.runner import SurveyContext, SurveyWorkflow
from django.conf import settings 
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

PROFILE_SURVEY = getattr(settings, 'POLLSTER_USER_PROFILE_SURVEY', 'intake')

class InfluenzanetWorkflow(SurveyWorkflow):
    
    def before_run(self, context):
        shortname = context.survey
        if shortname != PROFILE_SURVEY:
            su = context.survey_user
            if not self.user_has_data(PROFILE_SURVEY, su):
                return HttpResponseRedirect(self.get_survey_url(PROFILE_SURVEY, su))
        
            
    
