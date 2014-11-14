from apps.pollster.runner import DEBUG
from apps.survey.workflow import SurveyWorkflow
from apps.grippenet.models import PregnantCohort, Participation

PREGNANT_QUESTION = 'Q12'
PREGNANT_RESPONSE_YES = 0
PREGNANT_RESPONSE_NO = 1

class PregnantWorkflow(SurveyWorkflow):
    
    def before_run(self, context):
        survey_user = context.survey_user
        pregnant = None
        try:
            pregnant = PregnantCohort.objects.get(survey_user=survey_user)
        except PregnantCohort.DoesNotExist:
            pass
        context.pregnant = pregnant

    def create_pregnant(self, survey_user):
        part = None
        try:
            part = Participation.objects.get(survey_user=survey_user)
        except Participation.DoesNotExist:
            pass
        pregnant = PregnantCohort.objects.create(survey_user=survey_user)
        if part is None:
            # If new participant of this season
            pregnant.change_channel = True
        else:
            # If participant from previous years, consider standard channel
            pregnant.change_channel = False
        pregnant.save()
        return pregnant
    def before_save(self, context):
        shortname = context.survey.shortname
        is_ggnet = False
        change_channel = False # Do we need to change the channel field value
        if context.pregnant is not None:
            if DEBUG:
                self.debug("Already Subscriber to pregnant cohort")
            is_ggnet = True
            change_channel = context.pregnant.change_channel
        form = context.form
        if shortname == "intake":
            if not is_ggnet:
                if form.cleaned_data[PREGNANT_QUESTION] == PREGNANT_RESPONSE_YES:
                    if DEBUG:
                        self.debug("Subscribing to pregnant cohort")
                    is_ggnet = True
                    pregnant = self.create_pregnant(context.survey_user)
                    context.pregnant = pregnant
                    change_channel = pregnant.change_channel
        if change_channel:
            # Update the "channel" field in model instance
            setattr(form.instance, 'channel', 'G')
            if DEBUG:
                self.debug("Setting channel to G")
                 
             
        
         
        