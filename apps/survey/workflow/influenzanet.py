##
# Default Workflow for influenzaNet
##
from django.conf import settings 
from django.http import HttpResponseRedirect

from . import SurveyWorkflow

PROFILE_SURVEY = getattr(settings, 'POLLSTER_USER_PROFILE_SURVEY', 'intake')

class InfluenzanetWorkflow(SurveyWorkflow):
    """
        Influenzanet survey workflow
    """
    
    def before_run(self, context):
        """
            Check if user has a profile survey, run it if none.
        """
        shortname = context.survey.shortname
        if shortname != PROFILE_SURVEY:
            su = context.survey_user
            if not self.user_has_data(PROFILE_SURVEY, su):
                return HttpResponseRedirect(self.get_survey_url(PROFILE_SURVEY, su, next_survey=shortname))
        
            
    
