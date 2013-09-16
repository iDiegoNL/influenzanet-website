from django import template
import time

register = template.Library()

@register.tag(name="cache_killer")
def do_cache_killer(parser, token):
    try:
        tag_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag has no arguments" % token.contents.split()[0])
    return CacheKillerNode()

class CacheKillerNode(template.Node):
    def render(self, context):
        return u"?ck=" + unicode(int(time.mktime(time.gmtime())))

