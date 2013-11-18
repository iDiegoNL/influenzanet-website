from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import connection,transaction
from django.core.urlresolvers import reverse
from django.contrib import messages
from apps.survey.utils import get_db_type
from apps.survey.models import SurveyUser
from apps.survey.views import _decode_person_health_status, get_active_survey_user, _get_avatars, is_wait_launch
from apps.dashboard.models import UserBadge, Badge

from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist

DASHBOARD_USE_BADGE = getattr(settings, 'DASHBOARD_USE_BADGE', False)

BADGE_DISABLE_FEATURE = 'disable'

def render_template(name, request, context=None):
    return render_to_response('dashboard/'+name+'.html', context, context_instance=RequestContext(request) )

def _get_participants(user):
    """
    Get all registered and active participants in an household
    """
    data = SurveyUser.objects.filter(user=user, deleted=False)
    participants = {}
    for d in data:
        participants[d.global_id] = d
    return participants

def _get_participant_health_history(user_id, global_id, limit=None):
    results = []
    cursor = connection.cursor()
    table = 'pollster_results_weekly'
    params = { 'user_id': user_id, 'global_id': global_id }
    if limit:
        limit = " LIMIT %d " % limit
    else:
        limit = ''
    queries = {
        'sqlite':"""
            SELECT W.timestamp, S.status
              FROM pollster_health_status S, """ + table + """ W
             WHERE S.pollster_results_weekly_id = W.id
               AND W.user = :user_id AND W.global_id = :global_id
             ORDER BY W.timestamp DESC""" + limit,
        'mysql':"""
            SELECT W.timestamp, S.status
              FROM pollster_health_status S, """ + table + """ W
             WHERE S.pollster_results_weekly_id = W.id
               AND W.user = :user_id AND W.global_id = :global_id
             ORDER BY W.timestamp DESC""" + limit,
        'postgresql':"""
            SELECT W.timestamp, S.status
              FROM pollster_health_status S, """ + table + """ W
             WHERE S.pollster_results_weekly_id = W.id
               AND W.user = %(user_id)s AND W.global_id = %(global_id)s
             ORDER BY W.timestamp DESC""" + limit,
    }
    cursor.execute(queries[get_db_type(connection)], params)

    results = cursor.fetchall()
    for ret in results:
        timestamp, status = ret
        yield {'timestamp': timestamp, 'status': status, 'diag':_decode_person_health_status(status)}

def get_badges_context(participant, context):
    """
    Add badges information into view context, if needed
    """
    if DASHBOARD_USE_BADGE:
        manager = UserBadge.objects
        badges, names = manager.get_badges(indexed=True)
        
        # Check if badge feature is disabled for this participant
        if BADGE_DISABLE_FEATURE in names:
            b = names[BADGE_DISABLE_FEATURE]
            try:
                u = UserBadge.objects.get(participant=participant, badge=b)
                context['badges'] = None
                context['badge_disabled'] = True
                return
            except ObjectDoesNotExist:
                pass
         
        context['new_badges'] = manager.update_badges(participant)
        user_badges = manager.get_attributed_badges(participant=participant)
        
        # Only show badges with a state set to True
        showed_badges = []
        for u in user_badges:
            badge = badges[ u.badge_id ]
            if badge.visible:
                if u.state:
                    u.badge_ = badge
                    showed_badges.append(u)
        context['badges'] = showed_badges
            
    else:
        context['badges'] = None
        
def get_participant_profile(global_id):
    cursor = connection.cursor()
    cols = {
        'Q3':'zip_code',
    }
    select = '"' + '","'.join(cols.keys()) + '"'
    cursor.execute("""select %s from pollster_results_last_intake where global_id='%s'""" % (select, global_id))
    r = cursor.fetchone()
    i = 0
    d = {}
    for n in cols.itervalues():
        d[n] = r[i]
    return d 

@login_required
def index(request):
    if is_wait_launch(request):
        return HttpResponseRedirect(reverse('survey_wait_launch'))
    
    user_id = request.user.id
    participants =  _get_participants(request.user)
    global_id = request.GET.get('gid', None)
    
    context = {}
    
    if global_id:
        # Fetch participant health status history
        history = list(_get_participant_health_history(user_id, global_id, 5))
        context['history'] = history
        # participant = participants[global_id]
        # context['profile'] = get_participant_profile(global_id)
        context['use_badge'] = DASHBOARD_USE_BADGE
            
    context['avatars'] = _get_avatars(with_list=False)
    
    context['gid'] = global_id
    context['participants'] = participants
    context['url_group_management'] = reverse('group_management')
    
    return render_template('index', request, context)
    
@login_required
def badges(request):
    # user_id = request.user.id
    global_id = request.GET.get('gid', None)
    try:
        participant = get_active_survey_user(request)
    except:
        raise Http404()     
    context =  {}
    context['gid'] = global_id
    get_badges_context(participant, context)

    return render_template('ajax_dashboard', request, context)

@login_required
def badge_disable(request):
    
    user = request.user
    # global_id is used to redirect the user to his page
    global_id = request.GET.get('gid', None)
    
    badge = Badge.objects.get(name=BADGE_DISABLE_FEATURE)
    participants = _get_participants(request.user)
    if request.method == 'POST':
        disabled = request.POST.getlist(u'disable')
        if disabled is None:
            disabled = []
        
        @transaction.commit_on_success
        def update_disable(disabled):
            UserBadge.objects.filter(user=user, badge=badge).delete()
            for d in disabled:
                participant = int(d)
                b = UserBadge()
                b.badge = badge
                b.user_id = user.id
                if participant:
                    b.participant_id = participant
                else:
                    b.participant = None
                b.state = True # Always hide this badge
                b.save()
        
        update_disable(disabled)
        next = reverse('dashboard_index')
        if global_id:
            next += '?gid=' + global_id 
        return HttpResponseRedirect( next )
    
    disable_badges = list(UserBadge.objects.filter(user=user, badge=badge))
    
    disabled = []
    for d in disable_badges:
        if d.participant_id is None:
            disabled.append(0)
        else:
            disabled.append(d.participant_id)
    
    context = {
        'avatars' : _get_avatars(with_list=False),
        'participants':participants,
        'disabled': disabled,
    }
    
    return render_template('disable_badges', request, context)

@login_required
def badge_activate(request):
    global_id = request.GET.get('gid', None)
    try:
        participant = get_active_survey_user(request)
    except:
        raise Http404()     
    badge = Badge.objects.get(name=BADGE_DISABLE_FEATURE)
    UserBadge.objects.filter(participant=participant, badge=badge).delete()
    messages.add_message(request, messages.SUCCESS, "Badges feature have been reactivated for the participant %s" % participant.name)
    return HttpResponseRedirect(reverse('dashboard_index') + '?gid=' + global_id)
    