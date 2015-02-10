import urlparse, datetime

from django.conf.urls.defaults import url

from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication, BasicAuthentication, MultiAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import Resource
from tastypie.exceptions import NotFound
from tastypie.bundle import Bundle
from tastypie.serializers import Serializer

from apps.pollster import models
from apps.pollster import json

class UrlEncodedSerializer(Serializer):
    formats = ['json', 'jsonp', 'xml', 'yaml', 'html', 'plist', 'urlencoded']
    content_types = {
        'json': 'application/json',
        'jsonp': 'text/javascript',
        'xml': 'application/xml',
        'yaml': 'text/yaml',
        'html': 'text/html',
        'plist': 'application/x-plist',
        'urlencoded': 'application/x-www-form-urlencoded',
    }
        
    def from_urlencoded(self, data, options=None):
        qs = dict((k, v if len(v) > 1 else v[0])
                   for k, v in urlparse.parse_qs(data).iteritems())
        return qs

    def to_urlencoded(self, content): 
        pass
        
class ResultProxy(object):
    def __init__(self, shortname=None, global_id=None, last_participation_data=None):
        self.shortname = shortname
        self.global_id = global_id
        self.last_participation_data = last_participation_data
            
class ResultsEndpoint(Resource):
    last_participation_data = fields.DictField(attribute='last_participation_data', readonly=True, null=True, blank=True, use_in='detail')    
        
    class Meta:
        resource_name = 'results'
        object_class = ResultProxy
        always_return_data = True
        serializer = UrlEncodedSerializer()
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.global_id
            kwargs['shortname'] = bundle_or_obj.obj.shortname
        else:
            kwargs['pk'] = bundle_or_obj.global_id
            kwargs['shortname'] = bundle_or_obj.shortname

        return kwargs

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<shortname>[\w\d_-]+)/$" % self._meta.resource_name, 
                self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r"^(?P<resource_name>%s)/(?P<shortname>.+)/(?P<pk>[\w\d-]+)/$" % self._meta.resource_name, 
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),                
        ]
        
    def get_object_list(self, request):
        raise NotImplementedError()
        
    def obj_get_list(self, bundle, **kwargs):
        raise NotImplementedError()

    def obj_get(self, bundle, **kwargs):
        global_id = kwargs["pk"]
        try:
            survey = models.Survey.objects.get(shortname=kwargs["shortname"])
        except models.Survey.DoesNotExist:
            raise NotFound()
        return ResultProxy(kwargs["shortname"], global_id,
                           survey.get_prefill_data(bundle.request.user.id, global_id))
        
    def obj_create(self, bundle, **kwargs):
        global_id = bundle.request.GET.get("gid")
        try:
            survey = models.Survey.objects.get(shortname=kwargs["shortname"])            
        except models.Survey.DoesNotExist:
            raise NotFound()
            
        data = bundle.request.POST.copy()
        data['user'] = bundle.request.user.id
        data['global_id'] = global_id
        data['timestamp'] = datetime.datetime.now()
        form = survey.as_form()(data)
        if form.is_valid():
            form.save()
        else:
            pass
        return bundle
            
    def obj_update(self, bundle, **kwargs):
        raise NotImplementedError()

    def obj_delete_list(self, bundle, **kwargs):
        raise NotImplementedError()

    def obj_delete(self, bundle, **kwargs):
        raise NotImplementedError()

    def rollback(self, bundles):
        pass

