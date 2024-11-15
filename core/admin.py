from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Account

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'credits')

admin.site.register(Account, UserProfileAdmin)