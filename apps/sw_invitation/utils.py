from django.template.loader import render_to_string
from . import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.models import Site
from apps.partnersites.context_processors import site_context
from django.core.urlresolvers import reverse
from django.utils.html import strip_tags

def send_invitation(user, key, email, allow_user_mention=False):
    """
        user : the user who made the invitation
        key : key of the user
        email : invited email
        allow_user_mention: allow to include user email in the invitation
    """
    site = Site.objects.get_current()
    site_info = site_context()
    
    site_url = "https://%s"
    
    url = "%s/%s?invitation_key=%s" % (site_url, reverse('registration_register').strip('/'), key)
    
    site_info['site_logo'] = "%s/%s" % (site_url, site_info['site_logo'])
    
    if allow_user_mention:
        sender = " (%s) " % user.email
    else:
        sender = ' '  # default is a space (nothing to include)
    
    data = { 'email': email, 'key': key, 'url': url, 'allow_user_mention': allow_user_mention, 'sender':sender, 'site': site}
    data.update(site_info)
    
    template = settings.SW_INVITATION_EMAIL_INVITATION
    subject = render_to_string(template +'_subject.txt', dictionary=data)
    
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    
    html_content = render_to_string(template +'.html', dictionary=data)
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives()
    msg.subject = subject
    msg.body = text_content
    msg.to = [email]
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return True

def get_registration_signal():
    """
    get the registration signal from the configured module
    example registration.signals
    """
    user_registered = None
    if hasattr(settings, 'SW_INVITATION_SIGNAL_MODULE'):
        from django.utils.importlib import import_module
        module = import_module(settings.SW_INVITATION_SIGNAL_MODULE)
        user_registered = getattr(module,'user_registered')
    return user_registered
            
