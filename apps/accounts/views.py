from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from .forms import MySettingsForm

def index(request):
    return render_to_response('registration/index.html',
        context_instance=RequestContext(request))

@login_required
def my_settings(request):
    if request.method == "POST":
        form = MySettingsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            success = True
    else:
        form = MySettingsForm(instance=request.user)

    return render_to_response('accounts/my_settings.html', locals(), RequestContext(request))
