from datetime import datetime

from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core import serializers

from .models import MunicipalCodes;

def search(request):
   if request.method == "POST":
       zip = request.POST['zip']
       print zip
       codes = MunicipalCodes.objects.filter(zip=zip)
       data = serializers.serialize('json', codes);
       return HttpResponse(data, mimetype="application/javascript")
   id = request.GET['id'];
   return render_to_response('municipal/form.html',RequestContext(request,{'element_id': id}))