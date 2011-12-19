# -*- coding: utf-8 -*-
from cms.middleware.multilingual import has_lang_prefix, MultilingualURLMiddleware as Original, SUPPORTED

from ..models import UserReminderInfo

class MultilingualURLMiddleware(Original):
    def get_language_from_request (self, request):
        changed = False
        prefix = has_lang_prefix(request.path_info)
        if prefix:
            request.path = "/" + "/".join(request.path.split("/")[2:])
            request.path_info = "/" + "/".join(request.path_info.split("/")[2:])
            t = prefix
            if t in SUPPORTED:
                changed = True

        if not changed:
            if request.user.is_authenticated():
                qs = UserReminderInfo.objects.filter(user=request.user)
                if qs.count() == 1:
                    return qs.get().get_language()

        return Original.get_language_from_request(self, request)
