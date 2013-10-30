from django.template.loader import render_to_string, TemplateDoesNotExist
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse


def send_invitation(user, key, email, allow_user_mention=False):
    """
        user : the user who made the invitation
        key : key of the user
        email : invited email
        allow_user_mention: allow to include user email in the invitation
    """
    site = Site.objects.get_current()
    
    url = "https://%s/%s?invitation_key=%s" % (site.domain, reverse('registration_register').strip('/'), key)
    
    if allow_user_mention:
        sender = " (%s) " % user.email
    else:
        sender = ''  
    
    data = { 'email': email, 'key': key, 'url': url, 'allow_user_mention': allow_user_mention, 'sender':sender}
    
    template = getattr(settings, 'SW_INVITATION_EMAIL_INVITATION','sw_invitation/invitation_email')
    subject = render_to_string(template +'_subject.txt', dictionary=data)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    text_content = render_to_string(template +'.txt', dictionary=data)

    # Try to load an html version
    try:
        html_content = render_to_string(template +'.html', dictionary=data)
    except TemplateDoesNotExist:
        html_content = None 
    
    msg = EmailMultiAlternatives()
    msg.subject = subject
    msg.body = text_content
    msg.to = email
    if html_content is not None:
        msg.attach_alternative(html_content, "text/html")
    msg.send()
    return True

def get_registration_signal():
    user_registered = None
    if hasattr(settings, 'SW_INVITATION_SIGNAL_MODULE'):
        from django.utils.importlib import import_module
        module = import_module(settings.SW_INVITATION_SIGNAL_MODULE)
        user_registered = getattr(module,'user_registered')
    return user_registered
            
