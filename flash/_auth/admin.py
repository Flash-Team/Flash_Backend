from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from flash._auth.models import MyUser


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
    )