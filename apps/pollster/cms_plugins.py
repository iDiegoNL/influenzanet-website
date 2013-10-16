from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from apps.survey.models import SurveyUser
from apps.survey.views import _get_person_health_status
from .models import SurveyPlugin
from .models import SurveyChartPlugin
from .models import TranslationSurvey
from .utils import get_user_profile
from .fields import PostalCodeField
from .middleware import ForceResponse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import to_locale, get_language, ugettext as _
import locale, json, datetime, urllib, urlparse

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

    from apps.survey.views import _get_person_health_status


        # deal with the else branch somehow, since it's rather unexpected to have login_key in the
        # GET, yet have it be incorrect?

    # @login_required from this point on.


    def render(self, context, instance, placeholder):
        encoder = json.JSONEncoder(ensure_ascii=False, indent=2)
        request = context['request']
        global_id = request.GET.get('gid', None)
        issuccess = request.GET.get('success', False) and True
        isauthenticated = False

        # Only registered and logged users can submit a survey.
        if 'login_key' in request.GET:
            user = authenticate(key=request.GET['login_key'])
            if user is not None:
                login(request, user)
        if request.user.is_authenticated():
            isauthenticated = True

        # Setup all parameters needed both for GET and POST requests.
        language = get_language()
        locale_code = locale.locale_alias.get(language)
        survey_user = _get_active_survey_user(request)

        if isauthenticated:
            profile = None
            if global_id:
                profile = get_user_profile(request.user.id, global_id)
            survey = instance.survey
            if locale_code:
                locale_code = locale_code.split('.')[0].replace('_', '-')
                if locale_code == "en-US":
                    locale_code = "en-GB"
            translation = _get_object_or_none(TranslationSurvey, survey=survey, language=language, status="PUBLISHED")
            survey.set_translation_survey(translation)
            user_id = request.user.id
            global_id = survey_user and survey_user.global_id
            last_participation_data = survey.get_last_participation_data(user_id, global_id)

            # If this is a POST try to save the data and possibly display the result or redirect.
            form = None
            if request.method == 'POST':
                data = request.POST.copy()
                data['user'] = user_id
                data['global_id'] = global_id
                data['timestamp'] = datetime.datetime.now()
                form = survey.as_form()(data)
                if form.is_valid():
                    form.save()
                    # If we have an explicit redirect URL we redirect there, else we redirect
                    # on this very same page setting success to 1 to avoid multiple POSTs.
                    next_url = instance.redirect_path or request.path
                    next_url_parts = list(urlparse.urlparse(next_url))
                    query = dict(urlparse.parse_qsl(next_url_parts[4]))
                    query.update({'gid': global_id})
                    query.update({'success': 1})
                    next_url_parts[4] = urllib.urlencode(query)
                    next_url = urlparse.urlunparse(next_url_parts)
                    raise ForceResponse(HttpResponseRedirect(next_url))
                else:
                    survey.set_form(form)

            context.update({
                "isauthenticated": True,
                "issuccess": issuccess,
                "language": language,
                "locale_code": locale_code,
                "survey": survey,
                "default_postal_code_format": PostalCodeField.get_default_postal_code_format(),
                "last_participation_data_json": encoder.encode(last_participation_data),                
                "form": form,
                "person": survey_user,
            })
            if issuccess:
                # Compatibility with old results.
                if survey.shortname == 'weekly':
                    _ignored, diagnosis = _get_person_health_status(request, survey, global_id)
                    context.update({"diagnosis": diagnosis})
                # Old data and render the succes template.
                context.update({ "success_data": last_participation_data })
                context.update({ "success_content": instance.render(context) })
        else:
            context.update({
                "isauthenticated": False,
                "language": language,
                "locale_code": locale_code,
                "person": survey_user,
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

