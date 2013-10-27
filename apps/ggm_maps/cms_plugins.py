from datetime import date, timedelta
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import GGMMapsPlugin

class CMSGGMMapsPlugin(CMSPluginBase):
    model = GGMMapsPlugin
    name = _('GGM Maps')
    render_template = "ggm_maps/home.html"
    
    def render(self, context, instance, placeholder):
        today = date.today()
        past = [today - timedelta(days=7 * i) for i in range(52)]

        context.update({
            'past': past,
        })
        return context

plugin_pool.register_plugin(CMSGGMMapsPlugin)
