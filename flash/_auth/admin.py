from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from flash._auth.models import MyUser


@admin.register(MyUser)
class MyUserAdmin(UserAdmin):

    def text_role(self, user):
        return '{} ({})'.format(user.text_role, user.role)

    text_role.short_description = 'role'

    list_display = ('username', 'first_name', 'last_name', 'phone_number', 'text_role', 'is_superuser')

    fieldsets = (
        (None, {
            'fields': (('username', 'password'), ('first_name', 'last_name'), 'phone_number',)
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ('role', 'is_superuser')
        }),
    )
