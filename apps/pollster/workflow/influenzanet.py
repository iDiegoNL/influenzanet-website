##
# Default Workflow for influenzaNet
##
from apps.pollster.runner import SurveyContext

class InfluenzanetWorkflow:
    
    def before_run(self, context):
        shortname = context.survey
        if shortname != 'intake':
            su = context.survey_user
            
    
