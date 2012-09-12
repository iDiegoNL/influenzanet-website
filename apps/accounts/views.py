from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from .forms import EmailSettingsForm, UsernameForm

def index(request):
    return render_to_response('registration/index.html',
        context_instance=RequestContext(request))

@login_required
def my_settings(request, form=None):
    assert form in [None, 'email', 'password', 'username']
    success = request.GET.get("success")

    if request.method == "POST":
        email_form = EmailSettingsForm(request.POST if form == 'email' else None, instance=request.user)
        password_form = SetPasswordForm(request.user, request.POST if form == 'password' else None)
        username_form = UsernameForm(request.POST if form == 'username' else None, instance=request.user)

        process_form = locals()[form + "_form"] 

        if process_form.is_valid():
            process_form.save()

            return HttpResponseRedirect(reverse(my_settings) + "?success=True")

    else:
        email_form = EmailSettingsForm(instance=request.user)
        password_form = SetPasswordForm(user=request.user)
        username_form = UsernameForm(instance=request.user)

    return render_to_response('accounts/my_settings.html', locals(), RequestContext(request))
