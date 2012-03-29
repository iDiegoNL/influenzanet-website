from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import get_hexdigest, check_password, User
from django.db import transaction
import utils
from .utils import create_token
from .logger import auth_notify
# Connect to login_in signal
# This allow us to set the real user id in session
from django.contrib.auth import user_logged_in

# Connect to auth login signal
def login_handler(sender,**kwargs):
    auth_notify('login_handler','ok')
    user = kwargs['user']
    request = kwargs['request']
    epiwork_user = user._epiwork_user
    request.session['epiwork_user'] = epiwork_user # store real user in session

user_logged_in.connect(login_handler)

class EpiworkUserManager(models.Manager):
    
    @transaction.commit_manually()
    def create_user(self, login, email, password):
        user = EpiworkUser()
        user.login = login
        user.email = email
        user.set_password(password)
        
        # Create a random username and a fake email
        dj_username = utils.random_string(30)
        dj_email = "%s@localhost" % (dj_username,)
        
        user.set_user(dj_username)
       
        try:
            django_user = User.objects.create_user(dj_username, dj_email)
            django_user.is_active = False
            django_user.save()
            user.save()
            transaction.commit()
        except:
            transaction.rollback()
            raise 
        return user

class EpiworkUser(models.Model):
    user = models.CharField(_('username'),max_length=255) # encrypted user name in auth_user
    email = models.CharField(_('e-mail address'),max_length=255) # encrypted email
    login = models.CharField(_('username'),max_length=255) # 
    password = models.CharField(_('password'),max_length=128) # sha1 hash
    token_password = models.CharField(max_length=40)
    token_activate = models.CharField(max_length=40)
    is_active = models.BooleanField(default=False)
    
    objects = EpiworkUserManager()
    
    # Get the user login
    def get_user(self):
        return self.user

    def set_user(self, username):
        self.user = username

    def set_password(self, raw_password):
        if raw_password is None:
            self.set_unusable_password()
        else:
            import random
            algo = 'sha1'
            salt = get_hexdigest(algo, str(random.random()), str(random.random()))[:5]
            hsh = get_hexdigest(algo, salt, raw_password)
            self.password = '%s$%s$%s' % (algo, salt, hsh)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
         
    def get_django_user(self):
        username = self.get_user()
        return User.objects.get(username=username)

    def create_token_password(self):
        token = create_token()
        self.token_password = token
        self.save()
        return token
    
    def create_token_activate(self):
        token = create_token()
        self.token_activate = token
        self.save()
        return token
    
    @transaction.commit_manually()
    def activate(self):
        self.is_active = True
        self.token_activate = ''
        dju = self.get_django_user()
        dju.is_active = True
        try:
            self.save()
            dju.save()
            transaction.commit()
            return True
        except:
            transaction.rollback()
            return False

    def personalize(self, user):
        user.username = self.login
        user.email = self.email

class FakedUser(User):
    class Meta:
        proxy = True
        """"
        """ 
        
    def save(self, force_insert=False, force_update=False, using=None):
        raise Exception
        """
            Fake User is readonly once authenticated this account
        """
    
    def safe_save(self, force_insert=False, force_update=False, using=None):
        self.save_base( force_insert=False, force_update=False, using=None)