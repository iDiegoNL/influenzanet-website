from django.template.loader import render_to_string, TemplateDoesNotExist
from django.conf import settings
from django.core.mail import EmailMultiAlternatives


def send_invitation(user, key, email):
    
    data = { 'email': email, 'key': key}
    
    template = getattr(settings, 'SW_INVITE_EMAIL_INVITATION','sw_invite/invitation_email')
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
    if hasattr(settings, 'SW_INVITE_SIGNAL_MODULE'):
        from django.utils.importlib import import_module
        module = import_module(settings.SW_INVITE_SIGNAL_MODULE)
        user_registered = getattr(module,'user_registered')
    return user_registered
            
