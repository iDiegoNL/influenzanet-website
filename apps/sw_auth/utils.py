
from django.utils.http import int_to_base36, base36_to_int
from datetime import date
from random import choice
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
             
def get_timestamp():
    tm = date.today() - date(2001, 1, 1)
    return tm.days

def random_string(length, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
    return ''.join([choice(allowed_chars) for i in range(length)])

def create_token():
    timestamp = get_timestamp()
    ts36 = int_to_base36(timestamp)
    token = ts36 + '-' + random_string(32)
    return token

def get_token_age(token):
    ts36, r = token.split("-")
    timestamp = base36_to_int(ts36)
    now = get_timestamp()
    return now - timestamp

def send_activation_email(user, site):
    token = user.create_token_activate()
    ctx_dict = { 
        'activation_key': token,
        'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
        'site': site 
    }
    subject = render_to_string('registration/activation_email_subject.txt', ctx_dict)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    message = render_to_string('registration/activation_email.txt', ctx_dict)
    
    send_mail(subject, message, None, [user.email])
