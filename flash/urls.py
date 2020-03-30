from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('flash._auth.urls')),
    path('order/', include('flash.order.urls')),
]
