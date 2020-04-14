from rest_framework_extensions.routers import ExtendedSimpleRouter

from flash.organization.views import OrganizationsViewSet, FilialsViewSet

router = ExtendedSimpleRouter()

(
    router.register('', OrganizationsViewSet, basename='organization').
    register(r'filial', FilialsViewSet, basename='filial', parents_query_lookups=['organization'])
)

urlpatterns = router.urls
