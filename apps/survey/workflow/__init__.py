from django.core.urlresolvers import reverse

from apps.pollster.runner import BaseWorkflow

class SurveyWorkflow(BaseWorkflow):
    """
        Survey Workflow
        This class hold specific methods for survey app
    """
    def get_survey_url(self, shortname, survey_user):
        """
            get a survey url 
            @todo this is survey app specific
        """
        url = reverse('survey_fill', {'shortname': shortname})
        url += '?gid=' + survey_user.global_id
        return url

