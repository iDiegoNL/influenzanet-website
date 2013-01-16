from django.contrib.auth.models import User
from django.template import Context, Template, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db import connection, transaction

def counter(request):
    def country_count(country):
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM (SELECT global_id FROM pollster_results_intake WHERE \"Qcountry\" = %s GROUP BY global_id) AS x", [country])
        row = cursor.fetchone()
        return row[0]

    def global_count():
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM (SELECT global_id FROM pollster_results_intake GROUP BY global_id) AS x", [])
        row = cursor.fetchone()
        return row[0]

    try:
        if request.GET.get('country'):
            return HttpResponse(str(country_count(request.GET.get('country'))))

        return HttpResponse(str(global_count()))
    except:
        return HttpResponse('-')
