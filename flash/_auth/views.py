import json

from django.http import JsonResponse
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny

from flash._auth.serializers import RegisterSerializer


@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    data = json.loads(request.body)
    serializer = RegisterSerializer(data=data)

    serializer.is_valid(raise_exception=True)
    serializer.save()

    return JsonResponse(serializer.data, status=201)
