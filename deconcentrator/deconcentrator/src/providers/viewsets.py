from rest_framework import viewsets
from .models import *
from .serializers import *


class MethodViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Method.objects.all()
    serializer_class = MethodSerializer


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

