from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from flash._auth.views import UserCreate

router = DefaultRouter()

router.register('register', UserCreate, basename='users')

urlpatterns = [
    path('login/', obtain_jwt_token)
]

urlpatterns += router.urls
