from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from flash._auth.models import MyUser


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone_number', 'role', 'is_superuser')

    fieldsets = (
        (None, {
            'fields': (('username', 'password'), ('first_name', 'last_name'), 'phone_number',)
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ('role', 'is_superuser')
        }),
    )
