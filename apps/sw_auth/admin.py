from django.contrib import admin
from .models import EpiworkUser

class EpiworkUserAdmin(admin.ModelAdmin):
    list_display = ['login','email','is_active']
    exclude = ('user','password',) 

admin.site.register(EpiworkUser, EpiworkUserAdmin)