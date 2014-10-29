from django.conf import settings
from django.core import exceptions
from apps.common.importlib import load_class_from_path
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.translation import get_language
from . import models, views, json, fields
import locale, datetime, urlparse, urllib
from django.template import RequestContext

def get_locale(language):
    locale_code = locale.locale_alias.get(language)
    if locale_code:
        locale_code = locale_code.split('.')[0].replace('_', '-')
        if locale_code == "en-US":
            locale_code = "en-GB"
    return locale_code

def as_json(data):
    encoder = json.JSONEncoder(ensure_ascii=False, indent=2)
    return encoder.encode(data)

def get_next_url(url, global_id):
    next_url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(next_url_parts[4]))
    query.update({'gid': global_id})
    next_url_parts[4] = urllib.urlencode(query)
    next_url = urlparse.urlunparse(next_url_parts)
    return next_url



class SurveyContext:
    """
        Running context for a survey
        
        Instance of this class is transmitted to survey hook methods 
        
    """
    
    def __init__(self, request, survey):
        self.request = request
        self.survey = survey
        self.survey_user = None
        self.form = None
        self.language = None 
        self.last_data = None
        self.template = 'pollster/survey_run.html'
        self.data = {}
    
    def add_data(self, name, value):
        self.data[name] = value
        
    def get_template_data(self):
        self.data.update({
          "language": self.language,
          "locale_code": get_locale(self.language),
          "survey": self.survey,
          "default_postal_code_format": fields.PostalCodeField.get_default_postal_code_format(),
          "last_participation_data_json": as_json(self.last_data),
          "form": self.form,
          "person": self.survey_user,
        })
        return self.data

class SurveyRunner:
    """
        Survey Runner Handler
    """
    def __init__(self):
        self.before_hooks = []
        self.before_save_hooks = []
        self.after_save_hooks = []
        self.before_render_hooks = []
           
    def load_hooks(self):
        configs = getattr(settings, 'POLLSTER_RUNNER_MIDDLEWARE', None)
        if configs is None:
            raise exceptions.ImproperlyConfigured('SurveyRunner not configured')
        for path in configs:
            hook = load_class_from_path(path)
            
            if hasattr(hook, 'before_run'):
                self.before_hooks.append(hook.before_run)
            if hasattr(hook, 'before_save'):
                self.before_save_hooks.append(hook.before_save)
            if hasattr(hook, 'after_save'):
                self.after_save_hooks.append(hook.after_save)
            if hasattr(hook, 'before_render'):
                self.before_render_hooks.append(hook.before_render)
                
    def run(self, request, shortname):
        use_cache = getattr(settings, 'POLLSTER_USE_CACHE', False)
        survey = get_object_or_404(models.Survey, shortname=shortname, status='PUBLISHED')
        if use_cache:
            survey.set_caching(True)
        
        survey_context = SurveyContext(request, survey)
        
        language = get_language()
        
        survey_context.language = language
        
        # Get survey user
        survey_user = views._get_active_survey_user(request)
        user_id = request.user.id
        global_id = survey_user and survey_user.global_id
        
        survey_context.survey_user = survey_user
        
        # Hooks for before save
        for hook_method in self.before_hook:
            response = hook_method(survey_context)
            if response and isinstance(response, HttpResponse):
                return response
        
        # Prepare survey to be run
        translation = views.get_object_or_none(models.TranslationSurvey, survey=survey, language=language, status="PUBLISHED")
        if use_cache:
            translation.prefetch_tranlations()
        survey.set_translation_survey(translation)
        
        form = None
        
        # Now check if response has been submitted
        if request.method == 'POST':
            data = request.POST.copy()
            data['user'] = user_id
            data['global_id'] = global_id
            data['timestamp'] = datetime.datetime.now()
            form = survey.as_form()(data)
            survey_context.form = form
            if form.is_valid():
                
                # Try before_save hooks
                for hook_method in self.before_save_hooks:
                    response = hook_method(survey_context)
                    if response and isinstance(response, HttpResponse):
                        return response
                
                # Now save the data
                form.save()
                
                # Ask for hooks for a response
                for hook_method in self.after_save_hooks:
                    response = hook_method(survey_context)
                    if response and isinstance(response, HttpResponse):
                        return response
                    if response and isinstance(response, basestring):
                        next = response
                
                if next:
                    next = self.get_next_url(next, global_id )
                return HttpResponseRedirect(next)
            else:
                survey.set_form(form)

        survey_context.last_data = survey.get_prefill_data(user_id, global_id)
                
        for hook_method in self.before_render_hooks:
            response = hook_method(survey_context)
                        
        return render_to_response(survey_context.template, survey_context.get_template_data(), context_instance=RequestContext(request))

        