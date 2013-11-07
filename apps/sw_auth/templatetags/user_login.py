from __future__ import absolute_import

from django.template import Library
from apps.sw_auth.models import FakedUser
register = Library()


def user_login(user):
    return isinstance(user, FakedUser)

register.filter('user_login', user_login)
