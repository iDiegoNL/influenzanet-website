from django.contrib.auth.models import User 

class UserProvider(object):
    """
    This class provides a proxy class to iter on user list
    without depends on django.auth User model
    It allows to use an alternate authentication model (where auth and user identity are not in django tables
    
    It returns a User django model object, but the assumption is that you cannot access directly to the user's data 
    from the django's User model. Some operation should be done to populate the User object with the user identiy
    
    This implementation only fetch data from the django User model 
     
    """    
    
    def __init__(self):
        self.users = User.objects.filter(is_active=True)  
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
