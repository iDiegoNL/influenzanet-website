from apps.pollster.runner import DEBUG
from apps.survey.workflow import SurveyWorkflow
from apps.survey import WEEKLY_SURVEY, THANKS_WEEKLY_SURVEY
from apps.grippenet.models import PregnantCohort, Participation

from django.conf import settings
from django.core.urlresolvers import reverse

AWARENESS_ITERATION = getattr(settings, 'AWARENESS_ITERATION', 0)
AWARENESS_SURVEY = 'awareness'

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

class AwarenessWorkflow(SurveyWorkflow):

    def before_save(self, context):
        shortname = context.survey.shortname
        if shortname == AWARENESS_SURVEY:
            setattr(context.form.instance, 'channel', str(AWARENESS_ITERATION))

    def after_save(self, context):
        shortname = context.survey.shortname

        self.debug(shortname)

        if shortname == AWARENESS_SURVEY:
            return reverse(THANKS_WEEKLY_SURVEY)

        self.debug('Awareness = ' + str(AWARENESS_ITERATION))

        if AWARENESS_ITERATION == 0:
            return None

        if shortname == WEEKLY_SURVEY:
            self.debug('Checking awareness  for user ' + str(context.survey_user))
            r = self.user_get_last_data(AWARENESS_SURVEY, context.survey_user)
            need_fill = True
            if r:
                last_channel = int(r.channel)

                self.debug('Last response was for iteration ' + str(last_channel))
                if last_channel >= AWARENESS_ITERATION:
                    # User has already responded to this iteration
                    need_fill = False
            self.debug(' Need fill' + str(need_fill))
            if need_fill:
                return self.get_survey_url(AWARENESS_SURVEY, context.survey_user)




