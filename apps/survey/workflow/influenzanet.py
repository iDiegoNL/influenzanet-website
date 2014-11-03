##
# Default Workflow for influenzaNet
##
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from . import SurveyWorkflow
from .. import PROFILE_SURVEY
from ..household import SurveyHousehold


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
                m = _(u'Before we take you to the symptoms questionnaire, please complete the short background questionnaire below. You will only have to complete this once.')
                messages.add_message(context.request, messages.INFO, m )
                return HttpResponseRedirect(self.get_survey_url(PROFILE_SURVEY, su, next_survey=shortname))
        
    def after_save(self, context):
        shortname = context.survey.shortname
        if shortname == PROFILE_SURVEY: 
            h = SurveyHousehold.get_household(context.request)
            h.profile_updated(context.request, context.survey_user.gid)  
        next_url = None
        if 'next' not in context.request.GET:
            if shortname == PROFILE_SURVEY:
                next_url = reverse('profile_thanks')
            elif shortname == "weekly":
                next_url = "/dashboard"
            else:
                next_url = reverse('survey_run_thanks', {"shortname": shortname})
        else:
            next_url = context.request.GET
        return next_url
        
    
