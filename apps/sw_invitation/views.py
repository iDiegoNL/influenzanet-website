from .models import Invitation
from django.core.validators import email_re
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.template import RequestContext, Context
from django.contrib.auth.decorators import login_required

def render_template(name, request, context=None):
    return render_to_response('sw_invitation/'+name+'.html',
                              context,
                              context_instance=RequestContext(request)
    )

@login_required
def invite(request):
    user = request.user
    if request.method == 'POST':
        email = request.POST['email']
        allow_user_mention = int(getattr(request.POST, 'allow_user_mention', 0))
        if not email_re.search(email):
            messages.add_message(request, messages.ERROR, _(u'Enter a valid e-mail address.'))
        else:
            try:
                key = Invitation.objects.invite(user, email, allow_user_mention)
                messages.add_message(request, messages.INFO, _(u'User has been invited'))
            except Invitation.AlreadyInvited:
                messages.add_message(request, messages.ERROR, _(u'User has already been invited by someone'))
    
    invitations = Invitation.objects.all().filter(user=user)
    
    return render_template('invite', request, {'user':user, 'invitations':invitations })      
        
        
    