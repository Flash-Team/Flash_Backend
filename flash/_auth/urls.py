from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from flash._auth.views import register, UserList, UserDetail, PasswordView

urlpatterns = [
    path('register/', register),
    path('login/', obtain_jwt_token),
    path('password/', PasswordView.as_view()),
    path('user/', UserList.as_view()),
    path('user/<int:pk>/', UserDetail.as_view()),
]

