from django.conf import settings

SW_INVITATION_SIGNAL_MODULE = getattr(settings, 'SW_INVITATION_SIGNAL_MODULE', 'registration.signals')

SW_INVITATION_KEY_LENGTH = getattr(settings, 'SW_INVITATION_KEY_LENGTH', 5)

SW_INVITATION_KEY_PREFIX = getattr(settings, 'SW_INVITATION_KEY_PREFIX', '')

SW_INVITATION_EMAIL_INVITATION = getattr(settings, 'SW_INVITATION_EMAIL_INVITATION','sw_invitation/invitation_email')