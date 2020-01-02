from rest_framework import serializers
from .models import *


class StrategySerializer(serializers.ModelSerializer):

    class Meta:
        model = Strategy
        fields = '__all__'


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):

    results = ResultSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = '__all__'


class ObjectiveSerializer(serializers.ModelSerializer):

    jobs = JobSerializer(many=True, read_only=True)

    class Meta:
        model = Objective
        fields = '__all__'


