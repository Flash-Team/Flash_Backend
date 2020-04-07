from django.urls import path

from flash.product.views import CategoriesView, CategoryView, ProductsListView, ProductListView

urlpatterns = [
    path('', CategoriesView.as_view()),
    path('<int:pk>/', CategoryView.as_view()),
    path('<int:pk>/product/', ProductsListView.as_view()),
    path('<int:pk2>/product/<int:pk>/', ProductListView.as_view()),
]
