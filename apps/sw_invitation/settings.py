from django.conf import settings



"""
module full qualified name to get the "user_registered" signal, for example "registration.signals"
"""
SW_INVITATION_SIGNAL_MODULE = getattr(settings, 'SW_INVITATION_SIGNAL_MODULE', 'registration.signals')

"""
size of the random part of the key generated for each user (default is 5)
"""
SW_INVITATION_KEY_LENGTH = getattr(settings, 'SW_INVITATION_KEY_LENGTH', 5)

"""
Add a prefix to each key
"""
SW_INVITATION_KEY_PREFIX = getattr(settings, 'SW_INVITATION_KEY_PREFIX', '')

"""
Path (relative to templates directory) of the template files for the email 
(at leat 2 files are excepted, [template_path].txt, [template_path]_subject.txt. 
One .html file could be provided to add an html-based part to the invitation email)
"""
SW_INVITATION_EMAIL_INVITATION = getattr(settings, 'SW_INVITATION_EMAIL_INVITATION','sw_invitation/invitation_email')

"""
Maximum number of invitation sendable from an account 
"""
SW_INVITATION_MAX = getattr(settings, 'SW_INVITATION_MAX', 100)