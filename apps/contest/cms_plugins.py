from datetime import date
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import ContestPlugin, Prediction

class CMSContestPlugin(CMSPluginBase):
    """
        Plugin class for the latest news
    """
    model = ContestPlugin
    name = _('Contest')
    render_template = "contest/main.html"
    
    def render(self, context, instance, placeholder):
        already_done = Prediction.objects.filter(user=context['request'].user).count()
        if not already_done:
            filename = "prijs_grafiek2011"
        else:
            filename = "prijs_grafiek_weergave2011"

        if date.today() > date(2012, 1, 25):
            filename = "prijs_grafiek_weergave2011" # no longer possible to enter results

        context.update({
            'filename': filename,
            'already_done': already_done,
        })
        return context

plugin_pool.register_plugin(CMSContestPlugin)
