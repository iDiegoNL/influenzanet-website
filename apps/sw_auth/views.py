from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail
from django.contrib.sites.models import get_current_site
from .forms import PasswordResetForm, RegistrationForm, SetPasswordForm
from django.http import HttpResponseRedirect
from apps.sw_auth.models import EpiworkUser
from django.conf import settings
from apps.sw_auth.utils import get_token_age


def render_template(name, request, context=None):
    return render_to_response('sw_auth/'+name+'.html',
                              context,
                              context_instance=RequestContext(request)
    )
    
def send_email_user(user, subject, template, context):
    t = get_template(template)
    send_mail(subject, t.render(Context(context)), None, [user.email])
    

@csrf_protect
def register_user(request):
    if(request.method == "POST"):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            user = EpiworkUser.objects.create_user(d['username'], d['email'], d['password1'])
            site = get_current_site(request)
            token = user.create_token_activate()
            ctx_dict = { 'activation_key': token,
                     'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                     'site': site }
            subject = render_to_string('registration/activation_email_subject.txt', ctx_dict)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            message = render_to_string('registration/activation_email.txt', ctx_dict)
            
            send_mail(subject, message, None, [user.email])
            return HttpResponseRedirect(reverse('registration_complete'))
    form = RegistrationForm()
    return render_template('registration_form', request, { 'form': form}) 
            

def activate_user(request, activation_key):
    try:
        age = get_token_age(activation_key)
        if(age < settings.ACCOUNT_ACTIVATION_DAYS):
            user = EpiworkUser.objects.get(token_activate=activation_key)
            user.activate()
            return HttpResponseRedirect(reverse('registration_activation_complete'))
    except EpiworkUser.DoesNotExist:
        user = None
    return render_template('activate', request)

@csrf_protect
def password_reset(request):
    if(request.method == "POST"):
        form = PasswordResetForm(request.POST)
        if( form.is_valid() ):
            user = form.users_cache
            current_site = get_current_site(request)
            site_name = current_site.name
            c = {
                'email': user.email,
                'domain': current_site.domain,
                'site_name': site_name,
                'token': user.create_token_password(),
                'protocol': request.is_secure() and 'https' or 'http',
            }
            
            send_email_user(user, _("Password reset on %s") % site_name, 'sw_auth/email_reset_password.html', c)
            
            post_reset_redirect = reverse('auth_password_reset_done')
            return HttpResponseRedirect(post_reset_redirect)
    form = PasswordResetForm()
    return render_template('password_reset', request, {'form': form})

@never_cache
def password_confirm(request, token=None):    
    """
    """
    assert token is not None
    try:
        age = get_token_age(token)
        if(age < settings.ACCOUNT_ACTIVATION_DAYS):
            user = EpiworkUser.objects.get(token_password=token)
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse('auth_password_reset_complete'))
            else:
                form = SetPasswordForm()
    except:
        pass

def password_done(request):
    """
    Nothing to do
    """
    
def password_complete(request):
    """
    """
    
    
def my_settings(request):
    """
    """
    
def index(request):
    """
    """
    
    