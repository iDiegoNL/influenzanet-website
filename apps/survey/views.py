# -*- coding: utf-8 -*-
from datetime import datetime

from django import forms
from django.template import Context, loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db import connection, transaction, DatabaseError
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.db import connection

from apps.survey import utils, models, forms
from apps.pollster import views as pollster_views
from apps.pollster import utils as pollster_utils
from .survey import ( Specification,
                      FormBuilder,
                      JavascriptBuilder,
                      get_survey_context, )
import apps.pollster as pollster
import pickle

survey_form_helper = None
profile_form_helper = None

def get_active_survey_user(request):
    gid = request.GET.get('gid', None)
    if gid is None:
        return None
    else:
        try:
            return models.SurveyUser.objects.get(global_id=gid,
                                                 user=request.user)
        except models.SurveyUser.DoesNotExist:
            raise ValueError()

def _get_all_health_status():
    return  {
        "NO-SYMPTOMS":                                  _('No symptoms'),
        "ILI":                                          _('Flu symptoms'),
        "COMMON-COLD":                                  _('Common cold'),
        "GASTROINTESTINAL":                             _('Gastrointestinal symptoms'),
        "ALLERGY-or-HAY-FEVER-and-GASTROINTESTINAL":    _('Allergy / hay fever and gastrointestinal symptoms'),
        "ALLERGY-or-HAY-FEVER":                         _('Allergy / hay fever'), 
        "COMMON-COLD-and-GASTROINTESTINAL":             _('Common cold and gastrointestinal symptoms'),
        "NON-SPECIFIC-SYMPTOMS":                        _('Other non-influenza symptons'),
    }

def _decode_person_health_status(status):
   d = _get_all_health_status()
   if status in d:
        return d[status]
   return _('Unknown')

def _get_person_health_status(request, survey, global_id):
    data = survey.get_last_participation_data(request.user.id, global_id)
    status = None
    if data:
        cursor = connection.cursor()
        params = { 'weekly_id': data["id"] }
        queries = {
            'sqlite':"""
            SELECT S.status
              FROM pollster_health_status S
             WHERE S.pollster_results_weekly_id = :weekly_id""",
            'mysql':"""
            SELECT S.status
              FROM pollster_health_status S
             WHERE S.pollster_results_weekly_id = :weekly_id""",
            'postgresql':"""
            SELECT S.status
              FROM pollster_health_status S
             WHERE S.pollster_results_weekly_id = %(weekly_id)s"""
        }
        cursor.execute(queries[utils.get_db_type(connection)], params)
        result = cursor.fetchone()
        status = result[0] if result else None
    return (status, _decode_person_health_status(status))

def _get_person_is_female(global_id, table="pollster_results_intake"):
    try:
        cursor = connection.cursor()
        queries = {
            'sqlite':"""SELECT Q1 FROM """ + table + """ WHERE global_id = %s""",
            'mysql':"""SELECT `Q1` FROM """ + table + """ WHERE `global_id` = %s""",
            'postgresql':"""SELECT "Q1" FROM """ + table + """ WHERE "global_id" = %s""",
        }
        cursor.execute(queries[utils.get_db_type(connection)], [global_id,])
        return cursor.fetchone()[0] == 1 # 0 for male, 1 for female
    except:
        return None

def _get_health_history(request, survey, table="pollster_results_weekly"):
    results = []
    cursor = connection.cursor()
    params = { 'user_id': request.user.id }
    queries = {
        'sqlite':"""
            SELECT W.timestamp, W.global_id, S.status
              FROM pollster_health_status S, """ + table + """ W
             WHERE S.pollster_results_weekly_id = W.id
               AND W.user = :user_id
             ORDER BY W.timestamp DESC""",
        'mysql':"""
            SELECT W.timestamp, W.global_id, S.status
              FROM pollster_health_status S, """ + table + """ W
             WHERE S.pollster_results_weekly_id = W.id
               AND W.user = :user_id
             ORDER BY W.timestamp DESC""",
        'postgresql':"""
            SELECT W.timestamp, W.global_id, S.status
              FROM pollster_health_status S, """ + table + """ W
             WHERE S.pollster_results_weekly_id = W.id
               AND W.user = %(user_id)s
             ORDER BY W.timestamp DESC""",
    }
    cursor.execute(queries[utils.get_db_type(connection)], params)

    results = cursor.fetchall()
    for ret in results:
        timestamp, global_id, status = ret
        survey_user = models.SurveyUser.objects.get(global_id=global_id)
        yield {'global_id': global_id, 'timestamp': timestamp, 'status': status, 'diag':_decode_person_health_status(status), 'survey_user': survey_user}


@login_required
def group_management(request):
    try:
        survey = pollster.models.Survey.get_by_shortname('weekly')
    except:
        raise Exception("The survey application requires a published survey with the shortname 'weekly'")
    Weekly = survey.as_model()
    try:
        survey_user = get_active_survey_user(request)
    except ValueError:
        pass

    if request.method == "POST":
        global_ids = request.POST.getlist('global_ids')

        for survey_user in request.user.surveyuser_set.filter(global_id__in=global_ids):
            if request.POST.get('action') == 'healthy':
                messages.add_message(request, messages.INFO, 
                    _(u'The participant "%(user_name)s" has been marked as healthy.') % {'user_name': survey_user.name})

                profile = pollster_utils.get_user_profile(request.user.id, survey_user.global_id)
                if not profile:
                    messages.add_message(request, messages.INFO, 
                        _(u'Please complete the background questionnaire for the participant "%(user_name)s" before marking him/her as healthy.') % {'user_name': survey_user.name})
                    continue

                Weekly.objects.create(
                    user=request.user.id,
                    global_id=survey_user.global_id,
                    Q1_0=True, # Q1_0 => "No symptoms. The other fields are assumed to have the correct default information in them.
                    timestamp=datetime.now(),
                )
            elif request.POST.get('action') == 'delete':
                survey_user.deleted = True
                survey_user.save()

    history = list(_get_health_history(request, survey))
    persons = models.SurveyUser.objects.filter(user=request.user, deleted=False)
    persons_dict = dict([(p.global_id, p) for p in persons])
    for item in history:
        item['person'] = persons_dict.get(item['global_id'])
    for person in persons:
        person.health_status, person.diag = _get_person_health_status(request, survey, person.global_id)
        person.health_history = [i for i in history if i['global_id'] == person.global_id][:10]
        person.is_female = _get_person_is_female(person.global_id)

    return render_to_response('survey/group_management.html', {'persons': persons, 'history': history, 'gid': request.GET.get("gid")},
                              context_instance=RequestContext(request))


@login_required
def group_archive(request, year=None):
    try:
        survey = pollster.models.Survey.get_by_shortname('weekly')
    except:
        raise Exception("The survey application requires a published survey with the shortname 'weekly'")

    if not getattr(settings, 'POLLSTER_HISTORICAL_WEEKLIES') or not getattr(settings, 'POLLSTER_HISTORICAL_INTAKES'):
        # unchecked assumptions:
        # these are both lists of tuples (year, existing-table-name) and they the LHS of each of the tuples is identical
        # across both lists.

        # also: the most recent (current) year/season is on top
        raise Exception("Configuration error: please configure POLLSTER_HISTORICAL_WEEKLIES and POLLSTER_HISTORICAL_INTAKES")

    if year:
        year = int(year)
    else:
        year = settings.POLLSTER_HISTORICAL_WEEKLIES[0][0]
    season = "%s - %s" % (year, year + 1)

    weekly_table = dict(settings.POLLSTER_HISTORICAL_WEEKLIES)[year]
    intake_table = dict(settings.POLLSTER_HISTORICAL_INTAKES)[year]

    seasons = reversed(
        [(year, "%s - %s" % (year, year + 1)) for (year, _) in settings.POLLSTER_HISTORICAL_WEEKLIES]
    )

    history = list(_get_health_history(request, survey, table=weekly_table))
    persons = models.SurveyUser.objects.filter(user=request.user, deleted=False)
    persons_dict = dict([(p.global_id, p) for p in persons])
    for item in history:
        item['person'] = persons_dict.get(item['global_id'])
    for person in persons:
        person.health_history = [i for i in history if i['global_id'] == person.global_id]
        person.is_female = _get_person_is_female(person.global_id, table=intake_table)

    return render_to_response('survey/group_archive.html', {'persons': persons, 'history': history, 'gid': request.GET.get("gid"), 'seasons': seasons, 'season': season},
                              context_instance=RequestContext(request))

@login_required
def thanks_profile(request):
    try:
        survey_user = get_active_survey_user(request)
    except ValueError:
        pass
    return render_to_response('survey/thanks_profile.html', {'person': survey_user},
        context_instance=RequestContext(request))

@login_required
def select_user(request, template='survey/select_user.html'):
    # select_user is still used in some cases: notably when there are unqualified calls to
    # 'profile_index'. So we've not yet removed this template & view.
    # Obviously it's a good candidate for refactoring.

    next = request.GET.get('next', None)
    if next is None:
        next = reverse(index)

    users = models.SurveyUser.objects.filter(user=request.user, deleted=False)
    total = len(users)
    if total == 0:
        survey_user = models.SurveyUser.objects.create(
            user=request.user,
            name=request.user.username,
        )
        url = '%s?gid=%s' % (next, survey_user.global_id)
        return HttpResponseRedirect(url)
        
    elif total == 1:
        survey_user = users[0]
        url = '%s?gid=%s' % (next, survey_user.global_id)
        return HttpResponseRedirect(url)

    return render_to_response(template, {
        'users': users,
        'next': next,
    }, context_instance=RequestContext(request))

@login_required
def index(request):
    # this is the index for a actual survey-taking
    # it falls back to 'group management' if no 'gid' is provided.
    # i.e. it expects gid to be part of the request!

    try:
        survey_user = get_active_survey_user(request)
    except ValueError:
        raise Http404()
    if survey_user is None:
        return HttpResponseRedirect(reverse(group_management))

    # Check if the user has filled user profile
    profile = pollster_utils.get_user_profile(request.user.id, survey_user.global_id)
    if profile is None:
        messages.add_message(request, messages.INFO, 
            _(u'Before we take you to the symptoms questionnaire, please complete the short background questionnaire below. You will only have to complete this once.'))
        url = reverse('apps.survey.views.profile_index')
        url_next = reverse('apps.survey.views.index')
        url = '%s?gid=%s&next=%s' % (url, survey_user.global_id, url_next)
        return HttpResponseRedirect(url)

    try:
        survey = pollster.models.Survey.get_by_shortname('weekly')
    except:
        raise Exception("The survey application requires a published survey with the shortname 'weekly'")

    next = None
    if 'next' not in request.GET:
        next = reverse(group_management) # is this necessary? Or would it be the default?

    return pollster_views.survey_run(request, survey.shortname, next=next)

@login_required
def profile_index(request):
    # this renders an 'intake' survey
    # it expects gid to be part of the request.

    try:
        survey_user = get_active_survey_user(request)
    except ValueError:
        raise Http404()
    if survey_user is None:
        url = '%s?next=%s' % (reverse(select_user), reverse(profile_index))
        return HttpResponseRedirect(url)

    try:
        survey = pollster.models.Survey.get_by_shortname('intake')
    except:
        raise Exception("The survey application requires a published survey with the shortname 'intake'")

    next = None
    if 'next' not in request.GET:
        next = reverse(thanks_profile)

    return pollster_views.survey_run(request, survey.shortname, next=next)

@login_required
def main_index(request):
    # the generalness of the name of this method reflects the mess that the various
    # indexes have become. 

    # this is the one that does the required redirection for the button 'my account'
    # and is also used in the reminder emails.

    # i.e. it redirects to group if there is a group, to the main index otherwise

    if models.SurveyUser.objects.filter(user=request.user, deleted=False).count() > 1:
        return HttpResponseRedirect(reverse(group_management))

    if models.SurveyUser.objects.filter(user=request.user, deleted=False).count() == 0:
        survey_user = models.SurveyUser.objects.create(
            user=request.user,
            name=request.user.username,
        )

    gid = models.SurveyUser.objects.get(user=request.user, deleted=False).global_id
    return HttpResponseRedirect(reverse(index) + '?gid=' + gid)

@login_required
def people_edit(request):
    try:
        survey_user = get_active_survey_user(request)
    except ValueError:
        raise Http404()
    if survey_user is None:
        url = '%s?next=%s' % (reverse(select_user), reverse(people_edit))
        return HttpResponseRedirect(url)
    elif survey_user.deleted == True:
        raise Http404()

    if request.method == 'POST':
        form = forms.AddPeople(request.POST)
        if form.is_valid():
            survey_user.name = form.cleaned_data['name']
            survey_user.save()

            return HttpResponseRedirect(reverse(group_management))

    else:
        form = forms.AddPeople(initial={'name': survey_user.name})

    return render_to_response('survey/people_edit.html', {'form': form},
                              context_instance=RequestContext(request))

@login_required
def people_remove(request):
    try:
        survey_user = get_active_survey_user(request)
    except ValueError:
        raise Http404()

    if survey_user is None:
        url = reverse(group_management)
        return HttpResponseRedirect(url)
    elif survey_user.deleted == True:
        raise Http404()

    confirmed = request.POST.get('confirmed', None)

    if confirmed == 'Y':
        survey_user.deleted = True
        survey_user.save()
   
        url = reverse(group_management)
        return HttpResponseRedirect(url)

    elif confirmed == 'N':
        url = reverse(group_management)
        return HttpResponseRedirect(url)

    else:
        return render_to_response('survey/people_remove.html', {'person': survey_user},
                              context_instance=RequestContext(request))

@login_required
def people_add(request):
    if request.method == 'POST':
        form = forms.AddPeople(request.POST)
        if form.is_valid():
            survey_user = models.SurveyUser()
            survey_user.user = request.user
            survey_user.name = form.cleaned_data['name']
            survey_user.save()

            messages.add_message(request, messages.INFO, 
                _('A new person has been added.'))

            next = request.GET.get('next', None)
            if next is None:
                url = reverse(group_management)
            else:
                url = '%s?gid=%s' % (next, survey_user.global_id)
            return HttpResponseRedirect(url)

    else:
        form = forms.AddPeople()

    return render_to_response('survey/people_add.html', {'form': form},
                              context_instance=RequestContext(request))


