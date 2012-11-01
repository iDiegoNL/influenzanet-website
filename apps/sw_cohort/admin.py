from django.contrib import admin
from .models import Cohort, Token

class TokenAdmin(admin.ModelAdmin):
    list_display  = ('cohort','token', 'usage_left','valid_until')


admin.site.register(Cohort)
admin.site.register(Token, TokenAdmin)