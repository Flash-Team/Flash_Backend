from django.urls import path
from rest_framework.routers import SimpleRouter

from flash.order.views import ProductsView, ProductView, OrdersViewSet

router = SimpleRouter()

router.register('', OrdersViewSet, basename='order')

urlpatterns = [
    path('<int:pk>/product/', ProductsView.as_view()),
    path('<int:pk2>/product/<int:pk>/', ProductView.as_view()),
]

urlpatterns += router.urls
