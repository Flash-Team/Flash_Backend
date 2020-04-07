from rest_framework_extensions.routers import ExtendedSimpleRouter

from flash.order.views import OrdersViewSet, ProductsViewSet

router = ExtendedSimpleRouter()

(
    router.register('', OrdersViewSet, basename='order').
    register(r'product', ProductsViewSet, basename='product', parents_query_lookups=['order'])
)

urlpatterns = router.urls
