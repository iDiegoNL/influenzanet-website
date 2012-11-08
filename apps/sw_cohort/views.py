# Create your views here.
from django.template import RequestContext, Context
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from apps.survey.models import SurveyUser
from django.contrib import messages
from .models import Token
from apps.sw_cohort.models import CohortUser
from django.contrib.auth.decorators import login_required
from django.db import transaction

from django.utils.translation import ugettext_lazy as _

def render_template(name, request, context=None):
    return render_to_response('sw_cohort/'+name+'.html',
                              context,
                              context_instance=RequestContext(request)
    )


@transaction.commit_manually()
def do_register(request, gid, token):
    cohort = None
    try:
        user = SurveyUser.objects.get(global_id=gid)
        token = Token.objects.get(token=token)
        token.consume()
        subscription = CohortUser()
        subscription.user = user
        subscription.cohort = token.cohort
        subscription.save()
        token.save()
        transaction.commit() 
        cohort = token.cohort
    except SurveyUser.DoesNotExist:
        messages.error(request, _('User does not exist'))
    except Token.DoesNotExist:
        messages.error(request, _('invalid token'))
    except Token.TokenException as e:
        messages.error(request, str(e))
    except:
        pass
    if not cohort or cohort is None:
        transaction.rollback()
    return cohort

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
        messages.error(request, 'User n')
        return redirect(reverse('cohort_form'))
    cohort = do_register(request, gid, token)
    return render_template('register', request, {'cohort':cohort })