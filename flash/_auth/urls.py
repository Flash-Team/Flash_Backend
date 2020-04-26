from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from flash._auth.views import register, UsersView, UserView, PasswordView

urlpatterns = [
    path('register/', register),
    path('login/', obtain_jwt_token),
    path('password/', PasswordView.as_view()),
    path('user/', UsersView.as_view()),
    path('user/<int:pk>/', UserView.as_view()),
]

