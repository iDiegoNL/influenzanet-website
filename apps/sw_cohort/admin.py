from django.contrib import admin
from .models import Cohort, Token
from django.http import HttpResponse

class TokenAdmin(admin.ModelAdmin):
    list_display  = ('cohort','token', 'usage_left','valid_until')

def export_tokens(modeladmin, request, queryset):
    out = ''
    for cohort in queryset:
        tt =  Token.objects.filter(cohort=cohort)
        for t in tt:
            out += t.token + "\n"
    response = HttpResponse(mimetype="text/csv")
    response.content = out        
    
export_tokens.short_description = ""
    
class CohortAdmin(admin.ModelAdmin):
    actions = [export_tokens]


admin.site.register(Cohort, CohortAdmin)
admin.site.register(Token, TokenAdmin)