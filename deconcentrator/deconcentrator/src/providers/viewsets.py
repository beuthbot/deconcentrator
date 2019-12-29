from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *


class MethodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Method.objects.all()
    serializer_class = MethodSerializer
    permission_classes = [AllowAny]


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = [AllowAny]

