from rest_framework import serializers
from .models import *


class GeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = General
        fields = '__all__'


class SoldierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soldier
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class Message:
    def __init__(self, message):
        self.message = message


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()
