import json

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.response import Response

from flash._auth.models import MyUser
from flash._auth.serializers import RegisterSerializer, UsersSerializer


@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = RegisterSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)

    return HttpResponse(status=405)


class UsersViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        return MyUser.objects.all()

    def get_serializer_class(self):
        return UsersSerializer

    def create(self, request, *args, **kwargs):
        return Response({'message': 'Not allowed create user here'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
