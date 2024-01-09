from rest_framework import serializers

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserSignUpSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()