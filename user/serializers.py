from rest_framework import serializers
from .models import User, Organisation
from django.contrib import auth
from django.contrib.auth import authenticate,login,logout
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['firstName', 'lastName', 'email', 'phone']

class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['firstName', 'lastName', 'email', 'password', 'phone','token']

    # def create(self, validated_data):
    #     return User.objects.create_user(**validated_data)
    

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ['password','email','token']
        read_only_fields = ['token']
    

class OrganisationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['name', 'description']

    def validate(self, data):
        if not data['name']:
            raise serializers.ValidationError({'name': 'Organisation name is required'})
        return data

