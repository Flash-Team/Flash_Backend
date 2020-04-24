from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('auth/', include('flash._auth.urls')),
                  path('order/', include('flash.order.urls')),
                  path('category/', include('flash.product.urls')),
                  path('organization/', include('flash.organization.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
