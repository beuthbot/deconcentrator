from rest_framework import serializers
from .models import *


class MethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Method
        fields = '__all__'


class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = '__all__'

