# Create your views here.
from django.template import RequestContext, Context
from django.shortcuts import render_to_response

def render_template(name, request, context=None):
    return render_to_response('sw_cohort/'+name+'.html',
                              context,
                              context_instance=RequestContext(request)
    )


def register(request):
    return render_template('register')