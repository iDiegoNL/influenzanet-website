from django.db import models
from django.contrib.auth.models import User
from random import choice
from .utils import send_invitation, get_registration_signal
from django.conf import settings

# Handle registration signal if configured
user_registered = get_registration_signal()

if user_registered is not None:
    
    def handle_registration(sender, **kwargs):
        # @TODO
        key = getattr(kwargs, 'invitation_key', None)
        if key is None:
            # Try to get the key in the request
            request = getattr(kwargs, 'request', None)
            if request is not None:
                key = getattr(request.POST, "invitation_key", None)
        
        if key is not None:
            # Try to find the key
            if Invitation.objects.use_key(key):
                return
        
        # Try to find the invitation by the email of the registred user
        registered_user = kwargs['user']
        email = registered_user.email
        email = email.lower()
        try:
            invitation = Invitation.get(email=email)
            user = invitation.user
            usage = InvitationUsage()
            usage.user = user
            usage.save()
        except Invitation.DoesNotExist:
            pass

    user_registered.connect(handle_registration)    

class InvitationKey(models.Model):
    """
    An Invitation key is used to provide a key to identify the user
    """
    user = models.OneToOneField(User)
    key = models.CharField(max_length=30, unique=True)

class InvitationManager(models.Manager):
    
    def create_key(self, user):
        """
        Try to set a random key for a user
        To limit collision, can try several times
        """
        length = getattr(settings, 'SW_INVITE_TOKEN_LENGTH', 5)
        prefix = getattr(settings, 'SW_INVITE_TOKEN_PREFIX', '')
        # get a random int 
        i = 10 # try a maximum of 10 times
        while i > 0:
            key = prefix + ''.join([choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') for i in range(length)])
            key.upper() # be sure all is in uppercase
            try:
                u = InvitationKey.objects.get(token=key)
            except InvitationKey.DoesNotExist:
                token = InvitationKey()
                token.user = user
                token.key = key
                token.save()
            --i
        return None

    def get_key(self, user):
        try:
            token = InvitationKey.objects.get(user=user)
        except InvitationKey.DoesNotExist:
            token = self.create_key(user)
        
        return token
    
    def invite(self, user, email):
        token = self.get_key(user)
        email = email.lower()
        invitation = Invitation()
        invitation.user = user
        invitation.email = email
        send_invitation(user, token, email)
        invitation.save()
        return token
    
    def use_key(self, key):
        key = key.upper()
        try:
            token = InvitationKey.objects.get(key=key)
            user = token.user
            usage = InvitationUsage()
            usage.user = user
            usage.save()
            return True
        except InvitationKey.DoesNotExist:
            pass
        return False

class Invitation(models.Model):

    objects = InvitationManager()

    """
    Invitation made by a user to friends
    """
    user = models.ForeignKey(User)
    email = models.EmailField(max_length=254)
    date = models.DateField(auto_now_add=True)
    
class InvitationUsage(models.Model):
    """
    Log invitation used by invited users for a User
    The user logged is the user who made the invitation
    """
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)