import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from flash._auth.models import MyUser
from flash._auth.serializers import RegisterSerializer, UsersSerializer


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = RegisterSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return HttpResponse(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class PasswordView(APIView):

    DEFAULT_PASSWORD = 'qwe'

    permission_classes = (IsAuthenticated,)

    def put(self, request):

        password = self.request.data.get('password')

        if not password:
            return Response({'password': 'This field is required'}, status=status.HTTP_400_BAD_REQUEST)

        self.request.user.set_password(password)

        self.request.user.save()

        return Response({'message': 'Password changed'}, status=status.HTTP_200_OK)

    def delete(self, request):

        self.request.user.set_password(self.DEFAULT_PASSWORD)

        self.request.user.save()

        return Response({'message': 'Default password set'}, status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return MyUser.objects.all()

    def get_serializer_class(self):
        return UsersSerializer

    def get_permissions(self):
        if self.request.user.is_anonymous:
            return IsAuthenticated(),
          
        if self.request.user.is_admin:
            return IsAuthenticated(),

        return IsAdminUser(),

    def create(self, request, *args, **kwargs):
        return Response({'message': 'Not allowed create user here'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
