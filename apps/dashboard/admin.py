from django.contrib import admin
from .models import Badge

class BadgeAdmin(admin.ModelAdmin):
    list_display  = ('name','label', 'datasource','season','attribute_to')


admin.site.register(Badge, BadgeAdmin)

