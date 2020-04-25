from django.contrib import admin

from flash.organization.models import Organization, Filial


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'logo', 'rating', 'manager',)
    search_fields = ('name', 'rating',)


@admin.register(Filial)
class FilialAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'organization',)
    search_fields = ('address',)
