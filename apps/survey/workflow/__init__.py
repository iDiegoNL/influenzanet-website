from django.core.urlresolvers import reverse

from apps.pollster.runner import BaseWorkflow

from urllib import urlencode

class SurveyWorkflow(BaseWorkflow):
    """
        Survey Workflow
        This class hold specific methods for survey app
    """
    def get_survey_url(self, shortname, survey_user, next_survey=None):
        """
            get a survey url 
        """
        url = reverse('survey_fill', kwargs={'shortname': shortname})
        params = {} 
        params['gid'] = survey_user.global_id
        if next_survey is not None:
            next = reverse('survey_fill', kwargs={'shortname': next_survey})
            params['next'] = next
        if len(params) > 0:
            url += '?' + urlencode(params)
        return url

