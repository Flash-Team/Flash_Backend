from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from flash._auth.models import MyUser
from flash._auth.serializers import UserSerializer


class UserCreate(viewsets.GenericViewSet, mixins.CreateModelMixin):

    permission_classes = (AllowAny, )
    authentication_classes = ()

    def get_queryset(self):
        return MyUser.objects.all()

    def get_serializer_class(self):
        return UserSerializer
