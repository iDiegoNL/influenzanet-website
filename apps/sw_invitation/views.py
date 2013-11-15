from .models import Invitation
from django.core.validators import email_re
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.utils.html import strip_tags,escape
from django.template import RequestContext, Context
from django.contrib.auth.decorators import login_required
from apps.sw_invitation.models import InvitationUsage, InvitationKey
from .utils import prepare_message, send_message
from . import settings as conf

def render_template(name, request, context=None):
    return render_to_response('sw_invitation/'+name+'.html',
                              context,
                              context_instance=RequestContext(request)
    )


def parse_form(request):
    emails = request.POST['emails']
    from_name = request.POST['name']
    from_name = escape(strip_tags(from_name))
    personnal_text = request.POST['personnal']
    personnal_text = escape(strip_tags(personnal_text))
    include_email = int(request.POST.get('include_email', 0))
    emails = emails.replace(' ', '') 
    emails = emails.split(',')
    e = []
    for email in emails:
        if not email_re.search(email):
            messages.add_message(request, messages.ERROR, _(u'"%s" is not a valid email address') % email)
        else:
            e.append(email)
    return (e, from_name, include_email, personnal_text)

@login_required
def invite(request):
    user = request.user
    # get invitations sent
    invitations = Invitation.objects.all().filter(user=user)
    if invitations.count() > conf.SW_INVITATION_MAX:
        return render_template('max_invitation', request)
    from_name = ''
    if request.method == 'POST':
        emails, from_name, include_email, personnal_text = parse_form(request)
        for email in emails:
            try:
                key = Invitation.objects.invite(user, email)
                m = prepare_message(user, key.key, email, include_email, from_name, personnal_text, request.is_secure)
                send_message(email, m)
                messages.add_message(request, messages.SUCCESS, _(u'Invitation sent for "%s"') % email)
            except Invitation.AlreadyInvited:
                messages.add_message(request, messages.ERROR, _(u'email "%s" has already been invited by someone') % email)
    
    usages = InvitationUsage.objects.filter(user=user).count()
    return render_template('invite', request, {'user':user,'from_name':from_name, 'invitations':invitations, 'usages': usages})      
        
@login_required
def preview(request):
    user = request.user
    if request.method == 'POST':
        emails, from_name, include_email, personnal_text = parse_form(request)
        email = emails[0]
        key = Invitation.objects.get_invitation_key(user)
        m = prepare_message(user, key.key, email, include_email, from_name, personnal_text, request.is_secure)
        return render_template('preview', request, {'user':user,'message':m})        
        