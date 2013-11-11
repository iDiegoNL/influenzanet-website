from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import connection

from apps.survey.utils import get_db_type
from apps.survey.models import SurveyUser
from apps.survey.views import _decode_person_health_status, get_active_survey_user, _get_avatars
from apps.dashboard.models import UserBadge

from django.http import Http404


DASHBOARD_USE_BADGE = getattr(settings, 'DASHBOARD_USE_BADGE', False)

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
    if DASHBOARD_USE_BADGE:
        manager = UserBadge.objects
        badges = manager.get_badges(indexed=True)
        context['new_badges'] = manager.update_badges(participant)
        user_badges = manager.get_attributed_badges(participant=participant)
        for u in user_badges:
            u.badge_ = badges[ u.badge_id ]
        context['badges'] = user_badges
    else:
        context['badges'] = None


@login_required
def index(request):
    user_id = request.user.id
    participants =  _get_participants(request.user)
    global_id = request.GET.get('gid', None)
    
    context = {}
    
    if global_id:
        # Fetch participant health status history
        history = list(_get_participant_health_history(user_id, global_id, 5))
        context['history'] = history
        participant = participants[global_id]
        
        context['use_badge'] = DASHBOARD_USE_BADGE
        #get_badges_context(participant, context)
        
    else:
        history = None    
    
    context['avatars'] = _get_avatars(with_list=False)
    
    context['gid'] = global_id
    context['participants'] = participants
    
    return render_template('index', request, context)
    
def badges(request):
    user_id = request.user.id
    global_id = request.GET.get('gid', None)
    try:
        participant = get_active_survey_user(request)
    except:
        raise Http404()     
    context =  {}
    context['gid'] = global_id
    get_badges_context(participant, context)

    return render_template('ajax_dashboard', request, context)