import datetime
from urllib import urlencode
from urllib2 import urlopen, HTTPError
from django.utils import simplejson
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authentication import MultiAuthentication
from tastypie.authentication import BasicAuthentication
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import Resource
from tastypie.exceptions import NotFound
from tastypie.models import ApiKey
from tastypie.bundle import Bundle
from social_auth.models import UserSocialAuth
from social_auth.utils import setting
from apps.pollster.models import NotifyToken

class ApiKeyProxy(object):
    def __init__(self, username=None, apikey=None):
        self.username = username     
        if apikey:
            self.key = apikey.key
        else:
            self.key = ''


class AccessEndpoint(Resource):
    key = fields.CharField(attribute='key')
    username = fields.CharField(attribute='username', null=True)
    
    class Meta:
        resource_name = 'access'
        object_class = ApiKeyProxy
        always_return_data = True
        authentication = MultiAuthentication(
            BasicAuthentication(), ApiKeyAuthentication())
        authorization = Authorization()

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.key
        else:
            kwargs['pk'] = bundle_or_obj.key

        return kwargs

    def get_object_list(self, request):
        keys = ApiKey.objects.filter(user=request.user)
        if len(keys) > 0:
            return [ApiKeyProxy(request.user.username, x) for x in keys]
        return []
        
    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def obj_get(self, bundle, **kwargs):
        keys = ApiKey.objects.filter(user=bundle.request.user)
        for key in keys:
            if str(key.key) == kwargs["pk"]:
                return ApiKeyProxy(bundle.request.user.username, key)
        raise NotFound()

    def obj_create(self, bundle, **kwargs):
        # Only one key is allowed per user.
        keys = ApiKey.objects.filter(user=bundle.request.user)
        if len(keys) == 1:
            bundle.obj = ApiKeyProxy(bundle.request.user.username, keys[0])
        else:
            bundle.obj = ApiKeyProxy(
                bundle.request.user.username, 
                ApiKey.objects.create(user=bundle.request.user))
        # If the user passed notify tokens, make sure to save/update them.
        atoken = bundle.data.get("atoken")
        itoken = bundle.data.get("itoken")
        if atoken or itoken:
            now = datetime.datetime.now()
            tokens = NotifyToken.objects.filter(user=bundle.request.user)
            if len(tokens) == 1:
                 if atoken:
                     tokens[0].atoken = atoken
                 if itoken:
                     tokens[0].itoken = itoken
                 tokens[0].updated = now
                 tokens[0].is_gcm_invalid = False
                 tokens[0].save()
            else:
                NotifyToken.objects.create(
                    user=bundle.request.user,
                    atoken=atoken,
                    itoken=itoken,
                    created=now,
                    updated=now)
        return bundle

    def obj_update(self, bundle, **kwargs):
        raise NotImplementedError()

    def obj_delete_list(self, bundle, **kwargs):
        raise NotImplementedError()

    def obj_delete(self, bundle, **kwargs):
        key = self.obj_get(bundle, **kwargs)
        if key:
            ApiKey.objects.filter(key=key.key).delete()

    def rollback(self, bundles):
        pass


class AccessFacebookEndpoint(Resource):
    key = fields.CharField(attribute='key', null=True)
    username = fields.CharField(attribute='username', null=True)
    access_token = fields.CharField(attribute='access_token', null=True)
    
    class Meta:
        resource_name = 'access_facebook'
        object_class = ApiKeyProxy
        always_return_data = True
        authentication = MultiAuthentication(
            BasicAuthentication(), ApiKeyAuthentication(), Authentication())
        authorization = Authorization()

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.username
        else:
            kwargs['pk'] = bundle_or_obj.username

        return kwargs

    def get_object_list(self, request):
        if not request.user.is_authenticated():
            raise NotFound("user isn't authenticated")        
        keys = ApiKey.objects.filter(user=request.user)
        if len(keys) > 0:
            return [ApiKeyProxy(request.user.username, x) for x in keys]
        return []
        
    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def obj_get(self, bundle, **kwargs):
        if not request.user.is_authenticated():
            raise NotFound("user isn't authenticated")        
        keys = ApiKey.objects.filter(user=bundle.request.user)
        for key in keys:
            if str(key.key) == kwargs["pk"]:
                return ApiKeyProxy(bundle.request.user.username, key)
        raise NotFound()
        
    def obj_create(self, bundle, **kwargs):
        access_token = bundle.data['access_token']
        if access_token:
            # Check that access_token really comes from Influweb application.
            params = {'access_token': access_token}
            url = "https://graph.facebook.com/app?" + urlencode(params)
            try:
                data = simplejson.load(urlopen(url))
            except HTTPError:
                raise NotFound("access_token doesn't match")                
            if data['id'] != setting('FACEBOOK_APP_ID', None):
                raise NotFound("access_token generated by unsupported application")
            # Check that user id is already registered in our database.            
            # We don't need to really authenticate the user, just to generate
            # an API key or retrieve one if existing.
            url = "https://graph.facebook.com/me?" + urlencode(params)
            try:
                data = simplejson.load(urlopen(url))
            except HTTPError:
                raise NotFound("access_token doesn't match")
            try:
                social_user = UserSocialAuth.objects.get(uid=data['id'])
                user = User.objects.get(id=social_user.user_id)
                keys = ApiKey.objects.filter(user=user)
                if len(keys) == 1:
                    bundle.obj = ApiKeyProxy(user.username, keys[0])
                else:
                    bundle.obj = ApiKeyProxy(user.username, ApiKey.objects.create(user=user))
            except:
                raise NotFound()
            # If the user passed notify tokens, make sure to save/update them.
            atoken = bundle.data.get("atoken")
            itoken = bundle.data.get("itoken")
            if atoken or itoken:
                now = datetime.datetime.now()
                tokens = NotifyToken.objects.filter(user=user)
                if len(tokens) == 1:
                     if atoken:
                         tokens[0].atoken = atoken
                     if itoken:
                         tokens[0].itoken = itoken
                     tokens[0].updated = now
                     tokens[0].is_gcm_invalid = False
                     tokens[0].save()
                else:
                    NotifyToken.objects.create(
                        user=user,
                        atoken=atoken,
                        itoken=itoken,
                        created=now,
                        updated=now)
        return bundle
    
    def obj_update(self, bundle, **kwargs):
        raise NotImplementedError()

    def obj_delete_list(self, bundle, **kwargs):
        raise NotImplementedError()

    def obj_delete(self, bundle, **kwargs):
        key = self.obj_get(bundle, **kwargs)
        if key:
            ApiKey.objects.filter(id=key.id).delete()

    def rollback(self, bundles):
        pass
