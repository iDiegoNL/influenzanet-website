# Create your views here.

from django.utils.translation import ugettext as _
from django.template import RequestContext, Context
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from apps.survey.models import SurveyUser
from django.contrib import messages
from .models import Token
from apps.sw_cohort.models import CohortUser
from django.contrib.auth.decorators import login_required
from django.db import transaction

def render_template(name, request, context=None):
    return render_to_response('sw_cohort/'+name+'.html',
                              context,
                              context_instance=RequestContext(request)
    )


@transaction.commit_manually()
def do_register(request, gid, token):
    subscription = None
    cohort = None
    try:
        user = SurveyUser.objects.get(global_id=gid)
        token = Token.objects.get(token=token)
        subscription = CohortUser()
        subscription.user = user
        subscription.cohort = token.cohort
        subscription.save()
        token.consume()
        transaction.commit() 
        cohort = token.cohort
    except SurveyUser.DoesNotExist:
        messages.error(request, _('User does not exist'))
    except Token.DoesNotExist:
        messages.error(request, _('invalid token'))
    except Token.TokenException as e:
        messages.error(request, str(e))
    except Exception:
        transaction.rollback()
        raise
    if not subscription or subscription is None or cohort is None :
        transaction.rollback()
    return subscription

@login_required
def form(request):
    users = SurveyUser.objects.filter(user=request.user, deleted=False)
    return render_template('form', request, { 'users':users} )

# register a user to a cohort
@login_required
def register(request):
    gid = request.GET.get('gid',None)
    token = request.GET.get('token', None)
    if token is None:
        messages.error(request, _('token not provided'))
    if gid is None or token is None:
        messages.error(request, 'User not provided')
        return redirect(reverse('cohort_form'))
    subscription = do_register(request, gid, token)
    cohort = getattr(subscription, 'cohort', None)
    user = getattr(subscription, 'user', None)
    if user:
        messages.info(request, _('The participant %s has been registred') % str(user))
    return render_template('register', request, {'cohort':cohort, 'user': user })