from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.core.mail import send_mail
from django.contrib.sites.models import get_current_site
from .forms import PasswordResetForm
from django.http import HttpResponseRedirect, QueryDict

import utils

def render_template(name, request, context):
    return render_to_response('sw_auth/'+name+'html',
                              context,
                              context_instance=RequestContext(request)
    )


    

def register_user(request):
    

def activate_user(request):
    

@csrf_protect
def password_reset(request):
    if(request.method == "POST"):
        form = PasswordResetForm(request.POST)
        if( form.is_valid() ):
            user = form.users_cache
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
            token = user.create_token_password()
            t = loader.get_template('sw_auth/email_reset_password.html')
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'user': user,
                'token': token,
                'protocol': request.is_secure() and 'https' or 'http',
            }
            post_reset_redirect = reverse('sw_auth.views.password_reset_done')
            send_mail(_("Password reset on %s") % site_name, t.render(Context(c)), None, [user.email])
            return HttpResponseRedirect(post_reset_redirect)
    form = PasswordResetForm()
    return render_template('password_reset', request, {'form': form})
    

def password_done(request):
    
    
def password_confirm(request):    
    
def password_complete(request):
    
    
def my_settings(request):
    
    
def index(request):
    
    