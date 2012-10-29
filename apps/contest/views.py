from datetime import date
from decimal import Decimal
from datetime import date, timedelta

from django.db import connection, transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required

from .models import Prediction, Week

@login_required
def prijs_grafiek(request): 
    result = "<grafiekinput>"
    result += "<meter_id>%s</meter_id>\n" % request.user.id
    result += "<naam>%s</naam>\n" % request.user.username

    for weeknr, percentage in ili_percentages():
        result += '<week nr="%s">%s</week>' % (weeknr, percentage)

    result += "</grafiekinput>"
    return HttpResponse(result, 'application/xml')


@login_required
def prijs_weergave(request):
    result = "<voorspelling>\n"
    result += "<meter_id>%s</meter_id>\n" % request.user.id
    result += "<naam>%s</naam>\n" % request.user.username

    prediction_qs = Prediction.objects.filter(user=request.user)
    if prediction_qs.count() == 1:
        prediction = prediction_qs.get()
        result += "<datum>%s</datum>\n" % prediction.date.strftime("%Y-%m-%d")

        for week in prediction.week_set.all():
            result += "<week nr=\"%s\">%s</week>\n" % (week.number, week.value if week.value else 0)
            
    result += "</voorspelling>\n"
    return HttpResponse(result, 'application/xml')

@login_required
@csrf_exempt
def relay2(request):
    if date.today() > date(2013, 12, 18):
        raise Exception("The contest is closed")

    if request.method == "GET":
        return HttpResponse("""<form method="POST" action="">
<input name="week1" value="3.32">
<input name="week2" value="3.51">
<input name="week3" value="3.37">
<input type="submit">
</form>
        """)

    prediction, created = Prediction.objects.get_or_create(user=request.user)
    if not created:
        return HttpResponse("prijsvraag al ingediend")

    for week_nr in range(1, 32):
        value = request.POST.get('week%s' % week_nr)    
        Week.objects.create(prediction=prediction, number=week_nr, value=value)

    return HttpResponseRedirect("/nl/prijsvraag/")


@staff_member_required
def winners(request):
    percentages = dict(ili_percentages())
    result = []
    
    for prediction in Prediction.objects.all():
        score = 0
        for week in prediction.week_set.all():
            if week <= 9:
                continue # no need; this info was available when the contest started

            if not percentages.get(week.number):
                continue
            score += pow(Decimal(week.value) - percentages[week.number], 2)# / pow(percentages[week.number], 2)

        result.append((score, prediction))

    result = sorted(result)
    result_str = ""
    result_str += 'percentages: %s<br>' % percentages

    for score, prediction in result:
        result_str += "%s (%s, %s)<br>" % (score, prediction.user.username, prediction.user.pk)

    result_str += "=====<br>"

    best_prediction = result[0][1]
    for week in best_prediction.week_set.all():
        if week.number <= 9:
            continue # no need; this info was available when the contest started

        if not percentages.get(week.number):
            continue
        this_part = pow(Decimal(week.value) - percentages[week.number], 2)# / pow(percentages[week.number], 2)
        result_str +=  "%s ?= %s, %s<br>" % (percentages[week.number], week.value, this_part)

    return HttpResponse(result_str)

def ili_percentages():
    begin = date(2012, 11, 18)
    end = date(2013, 5, 5)
    weeknr = 1

    cursor = connection.cursor()

    while begin + timedelta((weeknr - 1) * 7) <= end:
        this_begin = begin + timedelta((weeknr - 1) * 7)

        cursor.execute("""SELECT status, count(*) AS cnt

FROM pollster_health_status AS S,

(SELECT MAX(id) AS id, global_id 
FROM pollster_results_weekly
WHERE timestamp BETWEEN %s AND %s + 7
GROUP BY global_id
ORDER BY global_id DESC
) AS W

WHERE S.pollster_results_weekly_id = W.id

GROUP BY status
""", [this_begin, this_begin])

        rows = cursor.fetchall()
        illnesses = dict(rows)

        total = sum(illnesses.values())
        ili = illnesses.get("ILI", 0)

        if total == 0: 
            yield (weeknr, Decimal('0.00'))

        else:
            percentage = (100 * Decimal(ili) / Decimal(total)).quantize(Decimal('0.01'))
            yield (weeknr, percentage)

        weeknr += 1
