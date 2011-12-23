from django.contrib import admin
from .models import Prediction, Week

class WeekInline(admin.TabularInline):
    model = Week

class PredictionAdmin(admin.ModelAdmin):
    list_display = ("user", "date",)
    search_fields = ('user__username', 'user__email',)
    inlines = [WeekInline]

admin.site.register(Prediction, PredictionAdmin)
