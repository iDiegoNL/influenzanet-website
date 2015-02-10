import urlparse

from django.shortcuts import render

from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication, BasicAuthentication, MultiAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import Resource
from tastypie.exceptions import NotFound
from tastypie.bundle import Bundle
from tastypie.serializers import Serializer

from apps.pollster import models
        
class SurveyProxy(object):
    def __init__(self, survey=None, xml=None):
        self._survey = survey
        self.xml = xml
        if survey:
            self.shortname = survey.shortname
        else:            
            self.shortname = None        
    
class SurveyEndpoint(Resource):
    shortname = fields.CharField(attribute='shortname')
    xml = fields.CharField(attribute='xml', readonly=True, null=True, blank=True, use_in='detail')
    
    class Meta:
        resource_name = 'survey'
        object_class = SurveyProxy
        always_return_data = True
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.shortname
        else:
            kwargs['pk'] = bundle_or_obj.shortname

        return kwargs

    def get_object_list(self, request):
        return [SurveyProxy(x) for x in models.Survey.objects.filter(status='PUBLISHED')]
        
    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def obj_get(self, bundle, **kwargs):
        try:
            survey = models.Survey.objects.get(shortname=kwargs["pk"])            
        except models.Survey.DoesNotExist:
            raise NotFound()
        response = render(bundle.request, 'pollster/survey_export_it.xml', { "survey": survey }, content_type='application/xml')
        return SurveyProxy(survey, response.content)

    def obj_create(self, bundle, **kwargs):
        raise NotImplementedError()

    def obj_update(self, bundle, **kwargs):
        raise NotImplementedError()

    def obj_delete_list(self, bundle, **kwargs):
        raise NotImplementedError()

    def obj_delete(self, bundle, **kwargs):
        raise NotImplementedError()

    def rollback(self, bundles):
        pass

