from django.contrib import admin

from flash.organization.models import Organization, Filial


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'rating', 'manager',)


@admin.register(Filial)
class FilialAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'organization',)
