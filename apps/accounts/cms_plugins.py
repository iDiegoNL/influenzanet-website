from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext as _

class UserMenuPlugin(CMSPluginBase):
    name = _("User Menu")
    render_template = "accounts/partials/cms_usermenu.html"

    def render(self, context, instance, placeholder):
        return context

plugin_pool.register_plugin(UserMenuPlugin)

