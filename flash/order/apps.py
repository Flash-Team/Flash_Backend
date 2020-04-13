from django.apps import AppConfig


class OrderConfig(AppConfig):
    name = 'flash.order'

    def ready(self):
        import flash.order.signals
