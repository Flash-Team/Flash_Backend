from rest_framework_extensions.routers import ExtendedSimpleRouter
from django.urls import path

from flash.product.views import category_list, CategoryDetail
from flash.product.views import CategoriesViewSet, ProductsListViewSet

router = ExtendedSimpleRouter()

(
    router.register('', CategoriesViewSet, basename='category').
    register(r'product', ProductsListViewSet, basename='product', parents_query_lookups=['category'])
)

urlpatterns = router.urls

# urlpatterns = [
#     path('', category_list),
#     path('<int:pk>/', CategoryDetail.as_view()),
# ]