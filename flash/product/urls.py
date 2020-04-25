from rest_framework_extensions.routers import ExtendedSimpleRouter

from flash.product.views import CategoriesViewSet, ProductsListViewSet

router = ExtendedSimpleRouter()

(
    router.register('', CategoriesViewSet, basename='category').
    register(r'product', ProductsListViewSet, basename='product', parents_query_lookups=['category'])
)

urlpatterns = router.urls
