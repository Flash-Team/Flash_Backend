from django.apps import AppConfig


class ProductConfig(AppConfig):
    name = 'flash.product'

    def ready(self):
        import flash.product.signals
