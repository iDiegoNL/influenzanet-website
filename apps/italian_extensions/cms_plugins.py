from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext as _

class UserRegistrationPlugin(CMSPluginBase):
    name = _("User registration")
    render_template = "italian_extensions/cms_userregistration.html"

    def render(self, context, instance, placeholder):
        return context

plugin_pool.register_plugin(UserRegistrationPlugin)

