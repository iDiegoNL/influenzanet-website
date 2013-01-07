from __future__ import absolute_import

from django.template import Library
from django.core.cache import cache 
from apps.sw_auth.models import EpiworkUser, FakedUser
from django.contrib.auth.models import User
register = Library()


def user_login(user):
    if isinstance(user, FakedUser):
        return user.username
    elif isinstance(user, User):
        return 'Anonymous'

register.filter('user_login', user_login)
