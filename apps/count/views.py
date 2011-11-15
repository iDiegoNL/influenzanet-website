from django.contrib.auth.models import User
from django.template import Context, Template, RequestContext
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db import connection, transaction

def counter(request):
    def q_count(country):
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM pollster_results_intake WHERE \"Qcountry\" = %s", [country])
        row = cursor.fetchone()
        return row[0]

    count = User.objects.count()

    if request.GET.get('country'):
        surely_nl = q_count("NL")
        surely_be = q_count("BE")

        rest = count - surely_nl - surely_be

        if request.GET.get('country') == "NL":
            return HttpResponse(str(surely_nl + int(2/3.0 * rest)))
        if request.GET.get('country') == "BE":
            return HttpResponse(str(surely_be + int(1/3.0 * rest)))

    return HttpResponse(str(count))
