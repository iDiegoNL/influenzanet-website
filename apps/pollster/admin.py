from django.contrib import admin

from .models import RuleType, QuestionDataType, VirtualOptionType, Survey

admin.site.register(RuleType)
admin.site.register(QuestionDataType)
admin.site.register(VirtualOptionType)
admin.site.register(Survey)
