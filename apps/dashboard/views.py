from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import connection,transaction
from django.core.urlresolvers import reverse
from django.contrib import messages
from apps.survey.utils import get_db_type
from apps.survey.models import SurveyUser
from django.utils.translation import ugettext_lazy as _
from apps.survey.views import  get_active_survey_user, _get_avatars, is_wait_launch
from django.utils import simplejson

from apps.dashboard.models import UserBadge, Badge

from django.http import Http404, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from apps.pollster.models import Chart

DASHBOARD_USE_BADGE = getattr(settings, 'DASHBOARD_USE_BADGE', False)

BADGE_DISABLE_FEATURE = 'disable'

# Recode InfluenzaNet syndrom to pretty syndrom group
SYNDROM_ALIASES = {
        "NO-SYMPTOMS":'no-symptom',
        "ILI":'ili',     
        "COMMON-COLD":'cold',
        "GASTROINTESTINAL":'gastro',
        "ALLERGY-or-HAY-FEVER-and-GASTROINTESTINAL": 'non-specific',
        "ALLERGY-or-HAY-FEVER":'allergy', 
        "COMMON-COLD-and-GASTROINTESTINAL": 'non-specific',
        "NON-SPECIFIC-SYMPTOMS": 'non-specific',
}

SYNDROM_LABELS = {
        "no-symptom":   _('No symptoms'),
        "ili":          _('Flu symptoms'),
        "cold":         _('Common cold'),
        "gastro":       _('Gastrointestinal symptoms'),
        "allergy":      _('Allergy / hay fever'), 
        "non-specific": _('Other non-influenza symptons'),
        'unknown': _('Unknown'),
}

def render_template(name, request, context=None):
    return render_to_response('dashboard/'+name+'.html', context, context_instance=RequestContext(request) )


def _get_syndrom(status):
    if status in SYNDROM_ALIASES:
        return SYNDROM_ALIASES[status]
    else:
        return 'unknown'

def _get_participants(user):
    """
    Get all registered and active participants in an household
    """
    data = SurveyUser.objects.filter(user=user, deleted=False)
    participants = {}
    for d in data:
        participants[d.global_id] = d
    return participants

def _get_houshold_history(user_id):
    """
     Return one health status by participant and by day (take the last status if several)
    """
    query = """SELECT global_id, date_part('epoch',a_day), last_value("status") OVER win
        FROM (
        SELECT W.global_id, date_trunc('day', W.timestamp) as a_day, S.status
          FROM pollster_health_status S left join pollster_results_weekly W on 
                      S.pollster_results_weekly_id = W.id
                      WHERE W.user = %d
                      ORDER BY W.timestamp DESC
        ) a
        WINDOW win as (PARTITION BY global_id, a_day)"""
    cursor = connection.cursor()
    cursor.execute(query % user_id)
    results = cursor.fetchall()
    history = []
    for r in results:
        history.append({'gid': r[0], 'time':r[1], 'syndrom': _get_syndrom(r[2])  })
    return history
    

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
        syndrom = _get_syndrom(status)
        diag = SYNDROM_LABELS.get(syndrom)
        yield {'timestamp': timestamp, 'status': status,'syndrom': syndrom, 'diag': diag}

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
    select = [
        # '"Q3" as zip_code',
        'CASE WHEN "Q1"=0 THEN \'M\' WHEN "Q1"=1 THEN \'F\' ELSE \'NA\' END as gender',
        '"Q2" as date_birth'
    ]
    select = ','.join(select)
    cursor.execute( ("""select %s from pollster_results_last_intake where global_id='%s'""" % (select, global_id, ) ))
    r = cursor.fetchone()
    if not r:
        return {}
    desc = cursor.description
    columns = []
    for col in desc:
        columns.append(col[0])
    r = dict(zip(columns, r))
    return r 

@login_required
def index(request):
    if is_wait_launch(request):
        return HttpResponseRedirect(reverse('survey_wait_launch'))
    
    user_id = request.user.id
    participants =  _get_participants(request.user)
    global_id = request.GET.get('gid', None)
    
    context = {'profile': None}
    
    encoder = simplejson.JSONEncoder(ensure_ascii=False)
    if global_id:
        # Fetch participant health status history
        history = list(_get_participant_health_history(user_id, global_id, 5))
        history.reverse()
        context['history'] = history
        context['history_count'] = len(history) - 1
        last_health_status = ''
        if len(history) > 0:
            last_health_status = history[ len(history) - 1].get('syndrom');
            
        context['last_health_status'] = last_health_status 
        # participant = participants[global_id]
        context['profile'] = encoder.encode(get_participant_profile(global_id))
        context['current_participant'] = participants.get(global_id);
        context['use_badge'] = DASHBOARD_USE_BADGE
            
    else:
        history = _get_houshold_history(user_id)
        context['history'] = encoder.encode(history)
        context['chart'] = Chart.objects.get(shortname='canton_health')    
    
    context['avatars'] = _get_avatars(with_list=False)
    
    context['gid'] = global_id
    context['participants'] = participants
    context['url_group_management'] = reverse('group_management')
    context['health_status'] = SYNDROM_LABELS
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
    