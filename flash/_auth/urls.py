from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from flash._auth.views import register

urlpatterns = [
    path('register/', register),
    path('login/', obtain_jwt_token)
]