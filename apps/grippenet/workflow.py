from apps.pollster.runner import DEBUG
from apps.survey.workflow import SurveyWorkflow
from apps.grippenet.models import PregnantCohort

class PregnantWorkflow(SurveyWorkflow):
    
    def before_run(self, context):
        survey_user = context.survey_user
        part = None
        try:
            part = PregnantCohort.objects.get(survey_user=survey_user)
        except PregnantCohort.DoesNotExist:
            pass
        context.pregnant = part
        
    def before_save(self, context):
        shortname = context.survey.shortname
        is_ggnet = False
        if context.pregnant is not None:
            if context.pregnant.active:
                if DEBUG:
                    self.debug("Already Subscriber to pregnant cohort")
                is_ggnet = True
        
        if shortname == "intake":
            form = context.form
            if not is_ggnet:
                if form.cleaned_data['G1'] == 1:
                    if DEBUG:
                        self.debug("Subscribing to pregnant cohort")
                    is_ggnet = True
                    part = PregnantCohort.objects.create(survey_user=context.survey_user)
                    part.save()
                    context.pregnant = part
            else:
                if form.cleaned_data['G1'] == 0:
                    if DEBUG:
                        self.debug("Unsubscribing to pregnant cohort")
                    # Unsubscribe
                    context.pregnant.active = False
                    context.pregnant.save()
                    is_ggnet = False
        if is_ggnet:
            # Update the "channel" field in model instance
            setattr(form.instance, 'channel', 'G')
            if DEBUG:
                self.debug("Setting channel to G")
                 
             
        
         
        