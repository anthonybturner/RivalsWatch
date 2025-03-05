from rest_framework import serializers
from .models import Strategy, Tutorial

class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = Strategy
        fields = ['title', 'content']

class TutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutorial
        fields = ['title', 'youtube_url']