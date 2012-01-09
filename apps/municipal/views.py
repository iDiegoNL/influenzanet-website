from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.core import serializers

from .models import MunicipalCodes;

def search(request):
    if request.method == "POST":
        zip = request.POST['zip']
        codes = MunicipalCodes.objects.filter(zip=zip)
        data = serializers.serialize('json', codes);
        return HttpResponse(data, mimetype="application/javascript")
    id = request.GET['id'];
    return render_to_response('municipal/form.html',RequestContext(request,{'element_id': id}))
def title(request,code):
    municipal = MunicipalCodes.objects.filter(code=code)
    if(municipal.count() == 0):
        return HttpResponse(status=404)
    
    return HttpResponse(municipal[0].title)