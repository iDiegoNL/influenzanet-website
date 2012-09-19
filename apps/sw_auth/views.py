from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.template.loader import get_template
from django.core.mail import send_mail
from django.contrib.sites.models import get_current_site
from .forms import PasswordResetForm, RegistrationForm, SetPasswordForm, MySettingsForm
from django.http import HttpResponseRedirect
from apps.sw_auth.models import EpiworkUser
from django.conf import settings
from apps.sw_auth.utils import get_token_age, send_activation_email
from apps.sw_auth.logger import auth_notify
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from datetime import date, datetime

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
    form = None
    if(request.method == "POST"):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            auth_notify('register ok','form is valid')
            d = form.cleaned_data
            user = EpiworkUser.objects.create_user(d['username'], d['email'], d['password1'])
            site = get_current_site(request)
            send_activation_email(user, site)
            return HttpResponseRedirect(reverse('registration_complete'))
    if form is None:
        form = RegistrationForm()
    return render_template('registration_form', request, { 'form': form}) 
            

def activate_user(request, activation_key):
    try:
        age = get_token_age(activation_key)
        if(age < settings.ACCOUNT_ACTIVATION_DAYS):
            user = EpiworkUser.objects.get(token_activate=activation_key, is_active=False)
            user.activate()
            return HttpResponseRedirect(reverse('registration_activation_complete'))
    except EpiworkUser.DoesNotExist:
        user = None
    return render_template('activate', request)

def activate_complete(request):
    if hasattr(settings, 'SWAUTH_LAUNCH_DATE'):
        d = datetime.strptime(settings.SWAUTH_LAUNCH_DATE,'%Y-%m-%d')
        d = d.date()
        if date.today() >= d:
            d = None # dont show launch date after the date
    else:
        d = None
    return render_template('activation_complete', request, {'launch_date': d})

@csrf_protect
def password_reset(request):
    form = None
    if(request.method == "POST"):
        form = PasswordResetForm(request.POST)
        if( form.is_valid() ):
            has_several = len(form.users_cache) > 1
            for user in form.users_cache:
                current_site = get_current_site(request)
                site_name = current_site.name
                c = {
                    'has_several': has_several,
                    'username': user.login,
                    'email': user.email,
                    'domain': current_site.domain,
                    'site_name': site_name,
                    'token': user.create_token_password(),
                    'protocol': request.is_secure() and 'https' or 'http',
                }
                
                send_email_user(user, _("Password reset on %s") % site_name, 'sw_auth/password_reset_email.html', c)
            
            post_reset_redirect = reverse('auth_password_reset_done')
            return HttpResponseRedirect(post_reset_redirect)
    if form is None:
        form = PasswordResetForm()
    return render_template('password_reset_form', request, {'form': form})

@never_cache
def password_confirm(request, token=None):    
    """
    """
    assert token is not None
    form = None
    try:
        age = get_token_age(token)
        if(age < settings.ACCOUNT_ACTIVATION_DAYS):
            user = EpiworkUser.objects.get(token_password=token)
            form = None
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect(reverse('auth_password_reset_complete'))
            if form is None:
                form = SetPasswordForm(user)   
                print form 
            return render_template('password_reset_confirm', request, {'form': form})
    except EpiworkUser.DoesNotExist:
        pass
    return render_template('password_reset_error', request)
    

def password_done(request):
    """
    Nothing to do
    """
    
def password_complete(request):
    """
    """
    
@login_required    
def my_settings(request):
    """
    """
    try:
        epiwork_user = request.session['epiwork_user']
        if request.method == "POST":
            form = MySettingsForm(request.POST, instance=request.user, epiwork=epiwork_user)
            if form.is_valid():
                form.save()
                success = True
        else:
            form = MySettingsForm(instance=request.user, epiwork=epiwork_user)
    
        return render_to_response('sw_auth/my_settings.html', locals(), RequestContext(request))
    except KeyError:
        auth_notify('setting', 'No settings')
        return render_to_response('sw_auth/no_settings.html', locals(), RequestContext(request))
        
    

    
def index(request):
    """
    """
    
    
