
from apps.survey.workflow import SurveyWorkflow
from apps.grippenet.models import PregnantCohort

class PregnantWorklflow(SurveyWorkflow):
    
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
                is_ggnet = True
        
        if shortname == "intake":
            form = context.form
            if not is_ggnet:
                if form.cleaned_data['G1'] == '1':
                    is_ggnet = True
                    part = PregnantCohort.objects.create(survey_user=context.survey_user)
                    part.save()
                    context.pregnant = part
            else:
                if form.cleaned_data['G1'] == '0':
                    # Unsubscribe
                    context.pregnant.active = False
                    context.pregnant.save()
                    is_ggnet = False
        if is_ggnet:
            form.cleaned_data['channel'] = 'G' 
             
        
         
        