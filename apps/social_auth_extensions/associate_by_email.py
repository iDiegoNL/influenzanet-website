from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from social_auth.models import UserSocialAuth
from social_auth.exceptions import AuthException, AuthCanceled
from social_auth.backends.facebook import FacebookAuth

def associate_by_email(details, user=None, *args, **kwargs):
    """Return user entry with same email address as one returned on details."""
    if user:
        return None

    email = details.get('email')

    if email:
        # Try to associate accounts registered with the same email address,
        # only if it's a single object. AuthException is raised if multiple
        # objects are returned.
        try:
            return {'user': UserSocialAuth.get_user_by_email(email=email)}
        except MultipleObjectsReturned:
            # Avoid to associate but don't throw an error. This was instead:
            # raise AuthException(kwargs['backend'], 'Not unique email address.')
            pass
        except ObjectDoesNotExist:
            pass
    else:
        response = kwargs["response"]
        kwargs["auth"].revoke_token(response["access_token"], response["id"])
        raise AuthCanceled(kwargs['backend'], 'Email address not provided.')

