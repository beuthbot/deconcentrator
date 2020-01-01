from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from deconcentrator.viewsets import CreateListRetrieveViewSet
from .models import *
from .serializers import *


class StrategyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer
    permission_classes = [AllowAny]


class ObjectiveViewSet(CreateListRetrieveViewSet):
    queryset = Objective.objects.all()
    serializer_class = ObjectiveSerializer
    permission_classes = [AllowAny]


class JobViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [AllowAny]


class ResultViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [AllowAny]
