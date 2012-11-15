from django.contrib.auth import authenticate
from django.utils import simplejson
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

from apps.survey.models import SurveyUser
from loginurl.utils import create as create_login_key

def response(o):
    response = HttpResponse(simplejson.dumps(o),mimetype="application/json")

@csrf_exempt
def mobile_login(request):
    
    if request.method != "POST":
        r = {'error': True, 'error_code': 1, 'error_msg': 'request method must be POST'}
        return response(r) 

    user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
    if user is None:
        r = {'error': True, 'error_code': 2, 'error_msg': 'invalid login'}
        return response(r) 

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
    r = {'error': False, 'user': users, 'login_key': login_key.key}
    return response(r) 
