from tastypie import fields
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import Resource
from tastypie.exceptions import NotFound
from tastypie.models import ApiKey
from tastypie.bundle import Bundle

class AccessEndpoint(Resource):
    id = fields.IntegerField(attribute='id')
    key = fields.CharField(attribute='key')
    
    class Meta:
        resource_name = 'access'
        object_class = ApiKey
        always_return_data = True
        authentication = BasicAuthentication()
        authorization = Authorization()

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id

        return kwargs

    def get_object_list(self, request):
        keys = ApiKey.objects.filter(user=request.user)
        if len(keys) > 0:
            return list(keys)
        return []
        
    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def obj_get(self, bundle, **kwargs):
        keys = ApiKey.objects.filter(user=bundle.request.user)
        if len(keys) > 0:
            for key in keys:
                if str(key.id) == kwargs["pk"]:
                    return key
        raise NotFound()

    def obj_create(self, bundle, **kwargs):
        # Only one key is allowed per user.
        keys = ApiKey.objects.filter(user=bundle.request.user)
        if len(keys) == 1:
            bundle.obj = keys[0]
        else:
            bundle.obj = ApiKey.objects.create(user=bundle.request.user)
        return bundle

    def obj_update(self, bundle, **kwargs):
        return self.obj_create(bundle, **kwargs)

    def obj_delete_list(self, bundle, **kwargs):
        raise NotImplementedError()

    def obj_delete(self, bundle, **kwargs):
        key = self.obj_get(bundle, **kwargs)
        if key:
            ApiKey.objects.filter(id=key.id).delete()

    def rollback(self, bundles):
        pass

