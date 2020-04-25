from django.apps import AppConfig


class OrganizationConfig(AppConfig):
    name = 'flash.organization'

    def ready(self):
        import flash.organization.signals
