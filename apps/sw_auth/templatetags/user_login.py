from __future__ import absolute_import

from django.template import Library
from apps.sw_auth.models import FakedUser
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
register = Library()


def user_login(user):
    if isinstance(user, FakedUser):
        s = """<span class="user-login">%s</span><br/><span class="user-email">%s</span>""" % (user.username, user.email,)
        return mark_safe(s)
    elif isinstance(user, User):
        return _('Anonymous')

register.filter('user_login', user_login)
