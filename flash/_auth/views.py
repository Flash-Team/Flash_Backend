import json
import logging

from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from flash._auth.models import MyUser
from flash._auth.serializers import RegisterSerializer, UsersSerializer

LOG = logging.getLogger('info')


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = RegisterSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()
            LOG.info('User {} with role {} registered'.format(user.username, user.text_role))

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


class UserList(APIView):
    def get_permissions(self):
        if self.request.user.is_anonymous:
            return IsAuthenticated(),

        if self.request.user.is_admin:
            return IsAuthenticated(),

        return IsAdminUser(),

    def get(self, request):
        users = MyUser.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        LOG.error('Cannot create user here')
        return Response({'message': 'Not allowed create user here'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserDetail(APIView):
    def get_permissions(self):
        if self.request.user.is_anonymous:
            return IsAuthenticated(),

        if self.request.user.is_admin:
            return IsAuthenticated(),

        return IsAdminUser(),

    def get_object(self, pk):
        try:
            return MyUser.objects.get(pk=pk)
        except MyUser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UsersSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UsersSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
