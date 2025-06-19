from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['full_name'] = user.full_name

        return token
    
    def validate(self, attrs):
        email = attrs.get("email")
        password= attrs.get("password")

        # check if email exists
        try: 
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or password")
        
        # check if password is correct or not
        if not user.check_password():
            raise serializers.ValidationError("Invalid email or password")
        
        # check if this user is active or not
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")
        
        user_data = super().validate({
            "username": user.username, # bắt buộc để Simple JWT xử lý
            "password": password
        }) 

        user_data['user'] = {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name
        }

        return user_data