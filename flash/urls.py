from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('flash._auth.urls')),
    path('order/', include('flash.order.urls')),
    path('category/', include('flash.product.urls')),
    path('organization/', include('flash.organization.urls')),
]

# Register debug_toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
