from django.conf import settings
from django import http
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response
from django import forms
from django.contrib.auth import authenticate, login
from django.utils import simplejson
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db import connection
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse, NoReverseMatch

from apps.journal.models import Entry
from apps.survey.models import SurveyUser
from loginurl.utils import create as create_login_key

def server_error(request, template_name='500.html'):
    """
    500 error handler.

    Templates: `500.html`
    Context:
        MEDIA_URL
            Path of static media (e.g. "media.example.org")

    Django's standard 500 error handler does not serve MEDIA_URL correctly; this one does
    """
    t = loader.get_template(template_name)
    return http.HttpResponseServerError(t.render(Context({
        'MEDIA_URL': settings.MEDIA_URL
    })))

def test_search(request):
    class SearchForm(forms.Form):
        q = forms.CharField(label="Search")

    query = 'highlighted'
    page = {
        'object_list': [
            {'object': "Resultaat nr. 1", 'get_stored_fields': {'summary': 'this word is highlighted in some way'}},
            {'object': "Resultaat nr. 2", 'get_stored_fields': {'summary': 'this word is highlighted in some way'}},
            {'object': "Resultaat nr. 3", 'get_stored_fields': {'summary': 'this word is highlighted in some way'}},
        ],
        'previous_page_number': 1,
        'next_page_number': 3,
        'has_next': True,
        'has_previous': True,
    }
    form = SearchForm()
    return render_to_response('search/search.html', locals(), context_instance=RequestContext(request))


@csrf_exempt
def mobile_login(request):
    if request.method != "POST":
        return HttpResponse(simplejson.dumps({'error': True, 'error_code': 1, 'error_msg': 'request method must be POST'}), mimetype="application/json") 

    user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
    if user is None:
        return HttpResponse(simplejson.dumps({'error': True, 'error_code': 2, 'error_msg': 'invalid login'}), mimetype="application/json") 

    survey_users = SurveyUser.objects.filter(user=user)
    users = []
    for survey_user in survey_users:
        cursor = connection.cursor()
        cursor.execute("""SELECT MAX(timestamp) FROM pollster_results_weekly WHERE global_id = %s""", [survey_user.global_id])
        last_survey_date = cursor.fetchall()[0][0]
        if isinstance(last_survey_date, unicode): # sqlite
            last_survey_date = last_survey_date[:10]
        else: # psql
            last_survey_date = ("%4d-%02d-%02d" % (last_survey_date.year, last_survey_date.month, last_survey_date.day)) if last_survey_date else None

        users.append({
            'global_id': survey_user.global_id,
            'last_survey_date': last_survey_date,
            'name': survey_user.name,
        })
        
    login_key = create_login_key(user, None, None, None)
    
    return HttpResponse(simplejson.dumps({'error': False, 'user': users, 'login_key': login_key.key}), mimetype="application/json") 

class LatestEntriesFeed(Feed):
    title = "Influenzanet news"
    link = "/" # not correct, but not used
    description = "Influenzanet news"

    def items(self):
        return Entry.objects.order_by('-pub_date')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt

    def item_link(self, item):
        try:
            return reverse("news") + "/" + item.get_relative_url()
        except:
            return "/"
