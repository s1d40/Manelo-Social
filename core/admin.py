from django.contrib import admin

# Register your models here.

from .models import ManeloUser


class UserAdmin(admin.ModelAdmin):
    fields =   ('username', 'email', 'first_name', 'last_name', 'profile_picture')
    list_display = ['username', 'email', 'first_name', 'last_name', 'profile_picture']
    search_fields = [ 'username', 'email']
    ordering = [ 'username']
    

admin.site.register(ManeloUser, UserAdmin)
