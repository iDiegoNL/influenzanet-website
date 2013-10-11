from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import SurveyPlugin
from .models import SurveyChartPlugin
from .models import TranslationSurvey
from .utils import get_user_profile
from .fields import PostalCodeField
from django.utils.translation import to_locale, get_language, ugettext as _
import locale, json

def _get_object_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None

def _get_active_survey_user(request):
    gid = request.GET.get('gid', None)
    if gid is None or not request.user.is_active:
        return None
    else:
        return get_object_or_404(SurveyUser, global_id=gid, user=request.user)

class CMSSurveyPlugin(CMSPluginBase):
    model = SurveyPlugin
    name = _("Survey")
    render_template = "pollster/cms_survey.html"

    def render(self, context, instance, placeholder):
        encoder = json.JSONEncoder(ensure_ascii=False, indent=2)
        request = context['request']
        global_id = request.GET.get('gid', None)
        profile = None
        if global_id:
            profile = get_user_profile(request.user.id, global_id)

        survey = instance.survey
        language = get_language()
        locale_code = locale.locale_alias.get(language)
        if locale_code:
            locale_code = locale_code.split('.')[0].replace('_', '-')
            if locale_code == "en-US":
                locale_code = "en-GB"
        translation = _get_object_or_none(TranslationSurvey, survey=survey, language=language, status="PUBLISHED")
        survey.set_translation_survey(translation)
        survey_user = _get_active_survey_user(request)
        user_id = request.user.id
        global_id = survey_user and survey_user.global_id
        last_participation_data = survey.get_last_participation_data(user_id, global_id)
        last_participation_data_json = encoder.encode(last_participation_data)
        form = None

        context.update({
            "language": language,
            "locale_code": locale_code,
            "survey": survey,
            "default_postal_code_format": PostalCodeField.get_default_postal_code_format(),
            "last_participation_data_json": last_participation_data_json,
            "form": form,
            "person": survey_user
        })
        return context

plugin_pool.register_plugin(CMSSurveyPlugin)

class CMSSurveyChartPlugin(CMSPluginBase):
    model = SurveyChartPlugin
    name = _("Survey Chart")
    render_template = "pollster/cms_survey_chart.html"

    def render(self, context, instance, placeholder):
        request = context['request']
        global_id = request.GET.get('gid', None)
        profile = None
        if global_id:
            profile = get_user_profile(request.user.id, global_id)
        context.update({
            'profile': profile,
            'chart': instance.chart,
            'object': instance,
            'placeholder': placeholder
        })
        return context

plugin_pool.register_plugin(CMSSurveyChartPlugin)

