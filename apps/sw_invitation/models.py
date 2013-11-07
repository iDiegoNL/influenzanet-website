from django.db import models
from django.contrib.auth.models import User
from random import choice
from .utils import get_registration_signal
from . import settings
from django.utils.log import getLogger

from apps.accounts.provider import UserProvider
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

def get_logger():
    return getLogger('sw_invitation')

# Handle registration signal if configured
user_registered = get_registration_signal()

if user_registered is not None:
    def handle_registration(sender, **kwargs):
        logger = get_logger()
        # logger.debug('entering sw_invitation signal handling')
        key = kwargs.get('invitation_key', None)
        if not key:
            # logger.debug("look for invitation key in request ")
            # Try to get the key in the request
            request = kwargs.get('request', None)
            if request is not None:
                key = request.GET.get("invitation_key", None)
        # User who made the invitation
        user_from = None
        if key:
            user_from = Invitation.objects.user_from_key(key)
            if user_from:
                logger.debug("user found from key '%s'" % key)
        # Try to find the invitation by the email of the registered user
        registered_user = kwargs.get('user', None)
        if registered_user is None:
            logger.debug('no user')
            raise Exception('User not provided in signal')
        email = registered_user.email
        email = email.lower()
        try:
            invitation = Invitation.objects.get(email=email)
            logger.debug("invitation found for email %s" % email)
            # user_from is first find from the key
            # if key is not found (or empty), then search from user
            # if the email correspond to another invitation, we trust key in first place
            if user_from is None:
                user_from = invitation.user
            invitation.used = True
            invitation.save() # register the invitation is used
        except Invitation.DoesNotExist:
            logger.debug("invitation not found for email '%s'" % email)
            pass
        if user_from is not None:
            usage = InvitationUsage()
            usage.user = user_from
            usage.save()

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
        length = settings.SW_INVITATION_KEY_LENGTH
        prefix = settings.SW_INVITATION_KEY_PREFIX
        # get a random int 
        i = 10 # try a maximum of 10 times
        while i > 0:
            key = prefix + ''.join([choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') for i in range(length)])
            key.upper() # be sure all is in uppercase
            try:
                u = InvitationKey.objects.get(key=key)
            except InvitationKey.DoesNotExist:
                invitation_key = InvitationKey()
                invitation_key.user = user
                invitation_key.key = key
                invitation_key.save()
                return invitation_key
            --i
        return None

    def get_key(self, user):
        try:
            key = InvitationKey.objects.get(user=user)
        except InvitationKey.DoesNotExist:
            key = self.create_key(user)
        
        return key
    
    def invite(self, user, email):
        key = self.get_key(user)
        email = email.lower()
        
        try:
            # Check on registred user list
            provider = UserProvider()
            e = provider.get_by_email(email)
            # If user exists we raise already invited
            # For privacy reason we dont tell any more information
            raise Invitation.AlreadyInvited()
        except MultipleObjectsReturned:
            # get_by_email expect one result
            raise Invitation.AlreadyInvited()
        except ObjectDoesNotExist:
            pass
        
        try:
            i = self.get(email=email)
            raise Invitation.AlreadyInvited()
        except Invitation.DoesNotExist:
            invitation = Invitation()
            invitation.user = user
            invitation.email = email
            invitation.save()
        return key
    
    def user_from_key(self, key):
        key = key.upper()
        try:
            invitation_key = InvitationKey.objects.get(key=key)
            return invitation_key.user
        except InvitationKey.DoesNotExist:
            pass
        return None

class Invitation(models.Model):

    objects = InvitationManager()

    """
    Invitation made by a user to friends
    """
    user = models.ForeignKey(User)
    email = models.EmailField(max_length=254)
    date = models.DateField(auto_now_add=True)
    used = models.BooleanField(default=False)
    
    class AlreadyInvited(Exception):
        pass
    
class InvitationUsage(models.Model):
    """
    Log invitation used by invited users for a User
    The user logged is the user who made the invitation
    """
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
