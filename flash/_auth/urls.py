from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from flash._auth.views import register, UsersViewSet, PasswordView

router = DefaultRouter()

router.register('user', UsersViewSet, basename='users')

urlpatterns = [
    path('register/', register),
    path('login/', obtain_jwt_token),
    path('password/', PasswordView.as_view()),
]

urlpatterns += router.urls
