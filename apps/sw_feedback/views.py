
from .forms import *
from django.shortcuts import render_to_response, redirect
from django.core.mail import send_mail
from django.template import RequestContext
from .feedback import feeback_token

def feedback(request):
    r = feeback_token('FB-OJ74GAJD-85')
    return render_to_response('sw_feedback/feedback.html',{ 'response':r })

def tell_a_friend(request):
    if request.method == 'POST':
        form = TellAFriendForm(request.POST)
        form.initCaptcha(request.session['captcha'])
        if form.is_valid():
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message =  form.cleaned_data['message']
            return redirect(sent_to_friend)
    else:
        form = TellAFriendForm()
    value = form.updateCaptcha()
    print 'session %d' % value
    request.session['captcha'] = value
    return render_to_response('sw_feedback/tell_a_friend.html',RequestContext(request, {
        'form': form,
    }))
    
def sent_to_friend(request):
    return render_to_response('sw_feedback/sent.html')