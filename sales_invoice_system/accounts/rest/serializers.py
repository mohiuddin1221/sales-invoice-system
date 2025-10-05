from rest_framework import serializers
from accounts.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    def validate_email(self, value):
        if User.objects.filter(email = value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def validate(self,data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Password do not match")
        return data
    
    def create(self, validate_data):
        return User.objects.create(
            username = validate_data.get('username'),
            email = validate_data['email'],
            password = validate_data['password1']
            
        )







class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # important: login via email

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password")

        data = super().validate({"email": email, "password": password})
        data["access_token"] = data["access"]
        data["refresh_token"] = data["refresh"]
        data.pop("access")
        data.pop("refresh")
        return data
