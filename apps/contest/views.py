from decimal import Decimal
from datetime import date, timedelta

from django.db import connection, transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .models import Prediction, Week

@login_required
def main(request):
    already_done = Prediction.objects.filter(user=request.user).count()

    MEDIA_URL = settings.MEDIA_URL
    if not already_done:
        return HttpResponse("""<object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" 
codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,0,0" 
width="770" height="470" id="prijs_grafiek2011" align="middle">
<param name="allowScriptAccess" value="sameDomain" />
<param name="movie" value="prijs_grafiek2011.swf" />
<param name="quality" value="high" />
<param name="bgcolor" value="#ffffff" />
<embed src="%(MEDIA_URL)scontest/prijs_grafiek2011.swf" quality="high" bgcolor="#ffffff" width="770" height="470" 
name="prijs_grafiek2011" align="middle" allowScriptAccess="sameDomain" 
type="application/x-shockwave-flash" pluginspage="http://www.macromedia.com/go/getflashplayer" />
</object>""" % locals())

    return HttpResponse("""<object classid="clsid:d27cdb6e-ae6d-11cf-96b8-444553540000" 
codebase="http://download.macromedia.com/pub/shockwave/cabs/flash/swflash.cab#version=6,0,0,0" 
width="770" height="470" id="prijs_grafiek" align="middle">
<param name="allowScriptAccess" value="sameDomain" />
<param name="movie" value="prijs_grafiek_weergave2011.swf" />
<param name="quality" value="high" />
<param name="bgcolor" value="#ffffff" />
<embed src="%(MEDIA_URL)scontest/prijs_grafiek_weergave2011.swf" quality="high" bgcolor="#ffffff" width="770" height="470" 
name="prijs_grafiek_weergave2011" align="middle" allowScriptAccess="sameDomain" type="application/x-shockwave-flash" 
pluginspage="http://www.macromedia.com/go/getflashplayer" />
</object>""" % locals())


@login_required
def prijs_grafiek(request): 
    result = "<grafiekinput>"
    result += "<meter_id>%s</meter_id>\n" % request.user.id
    result += "<naam>%s</naam>\n" % request.user.username

    begin = date(2011, 11, 15)
    end = date(2012, 5, 1)
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
            result += '<week nr="%s">0.00</week>' % weeknr

        else:
            percentage = (100 * Decimal(ili) / Decimal(total)).quantize(Decimal('0.01'))
            result += '<week nr="%s">%s</week>' % (weeknr, percentage)

        weeknr += 1

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
            result += "<week nr=\"%s\">%s</week>\n" % (week.number, week.value)
            
    result += "</voorspelling>\n"
    return HttpResponse(result, 'application/xml')

@login_required
@csrf_exempt
def relay2(request):
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

    return HttpResponseRedirect("/")
