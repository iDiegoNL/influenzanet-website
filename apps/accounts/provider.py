from django.contrib.auth.models import User 
from django.conf import settings
from django.utils.importlib import import_module

if hasattr(settings, 'USER_PROVIDER_CLASS'):
    m = settings.USER_PROVIDER_CLASS
    mod_path, cls_name = m.rsplit('.', 1)
    try:
        module = import_module(mod_path)
        cls = getattr(module, cls_name)
    except ImportError:
        raise Exception("Invalid module name %s" % mod_path)
    except AttributeError:
        raise Exception("Unknown class name %s in module %s" %(cls_name, mod_path, ))
    
    UserProvider = cls
else:
    class UserProvider(object):
        """
        This class provides a proxy class to iter on user list
        without depends on django.auth User model
        It allows to use an alternate authentication model (where auth and user identity are not in django tables
        
        It returns a User django model object, but the assumption is that you cannot access directly to the user's data 
        from the django's User model. Some operation should be done to populate the User object with the user identiy
        
        This implementation only fetch data from the django User model 
         
        """    
        
        def __init__(self, users=None):
            """
            users = an eventual queryset of users to iterate from
            """
            if users is None:
                self.users = User.objects.filter(is_active=True)
            else:
                self.users = users  
            self.iter = None
        
        def __iter__(self):
            self.iter = self.users.__iter__()
            return self # return self to force use of our next() method
        
        def get_by_email(self, email):
            return User.objects.get(email__iexact=email)
        
        def get_by_login(self, login):
            return User.objects.get(username=login)
        
        def next(self): 
            return next(self.iter)    
