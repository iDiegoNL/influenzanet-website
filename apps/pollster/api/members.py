from django.db import connection

from tastypie import fields
from tastypie.authentication import MultiAuthentication
from tastypie.authentication import BasicAuthentication
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import Resource
from tastypie.exceptions import NotFound
from tastypie.models import ApiKey
from tastypie.bundle import Bundle

from apps.survey import models

def _get_gender_and_timestamp(global_id):
    try:
        curs = connection.cursor()
        curs.execute("""SELECT "Q1", "timestamp" FROM pollster_results_intake WHERE global_id = %s ORDER BY "timestamp" DESC LIMIT 1""", (global_id,))
        data = curs.fetchone()
        return (data[0] == 1 and 'F' or 'M', data[1])
    except:
        return ('', None);
        
def _get_health_history(global_id):
    try:
        curs = connection.cursor()
        curs.execute("""SELECT status, timestamp FROM pollster_dashboard_history 
                         WHERE timestamp >= '2013-11-1' 
                           AND global_id = %s
                         ORDER BY timestamp""", (global_id,))
        return [{ "status": x[0], "timestamp": x[1] } for x in curs.fetchall()]
    except:
        return [];

class SurveyUserProxy(object):
    def __init__(self, survey_user=None, email=None, gender_and_ts=None):
        self.survey_user = survey_user
        self.email = email
        if gender_and_ts:
            self.gender = gender_and_ts[0]
            self.last_intake_date = gender_and_ts[1]
        else:
            self.gender = None
            self.last_intake_date = None
        if survey_user:
            self.global_id = survey_user.global_id
            self.name = survey_user.name
            self.last_participation_date = survey_user.last_participation_date
        else:            
            self.global_id = ''
            self.name = ''
            self.last_participation_date = None
                        
class MembersEndpoint(Resource):
    global_id = fields.CharField(attribute='global_id')
    name = fields.CharField(attribute='name')
    last_participation_date = fields.DateTimeField(attribute='last_participation_date', null=True)
    health_history = fields.ListField(attribute='health_history', null=True, use_in='detail')
    error = fields.CharField(attribute='error', null=True, use_in='detail')
    
    class Meta:
        resource_name = 'members'
        object_class = SurveyUserProxy
        always_return_data = True
        authentication = MultiAuthentication(
            BasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()

    def dehydrate(self, bundle):
        if bundle.obj.email:
            bundle.data['email'] = bundle.obj.email
        if bundle.obj.gender:
            bundle.data['gender'] = bundle.obj.gender
        if bundle.obj.last_intake_date:
            bundle.data['last_intake_date'] = bundle.obj.last_intake_date
        return bundle
        
    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.global_id
        else:
            kwargs['pk'] = bundle_or_obj.global_id

        return kwargs

    def _get_proxy(self, request, global_id):
        proxies = self.get_object_list(request)
        proxy = None
        for p in proxies:
            if p.global_id == global_id:
                proxy = p
        if not proxy:
            raise NotFound()
        return proxy
        
    def get_object_list(self, request):
        members = models.SurveyUser.objects.filter(user=request.user, deleted=False).order_by('id')
        return (
            [SurveyUserProxy(members[0], request.user.email, _get_gender_and_timestamp(members[0].global_id))] + 
            [SurveyUserProxy(x, None, _get_gender_and_timestamp(x.global_id)) for x in members[1:]])
        
    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def obj_get(self, bundle, **kwargs):
        proxy = self._get_proxy(bundle.request, kwargs['pk'])
        proxy.health_history = _get_health_history(proxy.global_id)
        return proxy

    def obj_create(self, bundle, **kwargs):
        if models.SurveyUser.objects.filter(user=bundle.request.user, name=bundle.data['name'], deleted=False).count() > 0:
            bundle.obj = SurveyUserProxy()
            bundle.obj.error = "MEMBER-ALREADY-EXISTS"
            bundle.data = {}
            return bundle            
        survey_user = models.SurveyUser.objects.create(
            user=bundle.request.user,
            name=bundle.data['name'],
        )
        bundle.obj = SurveyUserProxy(survey_user)
        bundle.data = {}
        return bundle
        
    def obj_update(self, bundle, **kwargs):
        if models.SurveyUser.objects.filter(user=bundle.request.user, name=bundle.data['name'], deleted=False).count() > 0:
            bundle.obj.error = "MEMBER-ALREADY-EXISTS"
            bundle.data = {}
            return bundle            
        proxy = self._get_proxy(bundle.request, kwargs['pk'])
        proxy.survey_user.name = bundle.data['name']
        proxy.survey_user.save()
        proxy.name = proxy.survey_user.name
        bundle.obj = proxy
        bundle.data = {}        
        return bundle

    def obj_delete_list(self, bundle, **kwargs):
        raise NotImplementedError()

    def obj_delete(self, bundle, **kwargs):
        proxy = self._get_proxy(bundle.request, kwargs['pk'])
        proxy.survey_user.deleted = True
        proxy.survey_user.save()
        return bundle
        
    def rollback(self, bundles):
        pass

