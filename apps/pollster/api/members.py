from django.db import connection

from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication, BasicAuthentication, MultiAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import Resource
from tastypie.exceptions import NotFound
from tastypie.models import ApiKey
from tastypie.bundle import Bundle

from apps.survey import models

def _get_gender(global_id):
    try:
        curs = connection.cursor()
        curs.execute("""SELECT "Q1" FROM pollster_results_intake WHERE global_id = %s""", (global_id,))
        return curs.fetchone()[0] == 1 and 'F' or 'M'
    except:
        return '';

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
    def __init__(self, survey_user=None, email=None):
        self._survey_user = survey_user
        self.email = email
        if survey_user:
            self.global_id = survey_user.global_id
            self.name = survey_user.name
            self.last_participation_date = survey_user.last_participation_date
        else:            
            self.global_id = None
            self.name = None
            self.last_participation_date = None
                        
class MembersEndpoint(Resource):
    global_id = fields.CharField(attribute='global_id')
    name = fields.CharField(attribute='name')
    last_participation_date = fields.DateTimeField(attribute='last_participation_date', null=True)
    gender = fields.CharField(attribute='gender', use_in='detail')
    health_history = fields.ListField(attribute='health_history', use_in='detail')
    
    class Meta:
        resource_name = 'members'
        object_class = SurveyUserProxy
        always_return_data = True
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()

    def dehydrate(self, bundle):
        if bundle.obj.email:
            bundle.data['email'] = bundle.obj.email
        return bundle
        
    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.global_id
        else:
            kwargs['pk'] = bundle_or_obj.global_id

        return kwargs

    def get_object_list(self, request):
        members = models.SurveyUser.objects.filter(user=request.user).order_by('id')
        return (
            [SurveyUserProxy(members[0], request.user.email)] + 
            [SurveyUserProxy(x) for x in members[1:]])
        
    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def obj_get(self, bundle, **kwargs):
        try:
            member = models.SurveyUser.objects.get(global_id=kwargs["pk"], user=bundle.request.user)            
        except models.SurveyUser.DoesNotExist:
            raise NotFound()
        proxy = SurveyUserProxy(member)
        proxy.gender = _get_gender(member.global_id)
        proxy.health_history = _get_health_history(member.global_id)
        return proxy

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

