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

        context.update({
            'filename': filename,
        })
        return context

plugin_pool.register_plugin(CMSContestPlugin)
