from django.urls import path

from flash.order.views import OrdersView, OrderView, ProductsView, ProductView

urlpatterns = [
    path('', OrdersView.as_view()),
    path('<int:pk>/', OrderView.as_view()),
    path('<int:pk>/product/', ProductsView.as_view()),
    path('<int:pk2>/product/<int:pk>/', ProductView.as_view()),
]
