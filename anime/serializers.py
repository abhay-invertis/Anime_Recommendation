from rest_framework import serializers
from django.contrib.auth.models import User
from .models import WatchedAnime, Userpreference
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class WatchedAnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchedAnime
        fields = '__all__'

class UserpreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userpreference
        fields = '__all__'
