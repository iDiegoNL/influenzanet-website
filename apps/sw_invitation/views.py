from .models import Invitation
from django.core.validators import email_re
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.template import RequestContext, Context


def render_template(name, request, context=None):
    return render_to_response('sw_invite/'+name+'.html',
                              context,
                              context_instance=RequestContext(request)
    )


def invite(request):
    user = request.user
    if request.method == 'POST':
        email = request.method.POST['email']
        if not email_re.search(email):
            messages.add_message(request, messages.ERROR, _(u'Enter a valid e-mail address.'))
        else:
            if Invitation.objects.invite(user, email):
                messages.add_message(request, messages.INFO, _(u'User has been invited'))
    
    invitations = Invitation.objects.all().filter(user=user)
    
    return render_template('invite', request, {'user':user, 'invitations':invitations })      
        
        
    