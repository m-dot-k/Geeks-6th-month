from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from users.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.cache import cache
import random

class UserBaseSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)
    dob = serializers.DateField()
    password = serializers.CharField()


class AuthValidateSerializer(UserBaseSerializer):
    pass


class RegisterValidateSerializer(UserBaseSerializer):
    def validate_email(self, email):
        try:
            CustomUser.objects.get(email=email)
        except:
            return email
        raise ValidationError('Email уже существует!')



class ConfirmationSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)
    email = serializers.EmailField()

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        code = attrs.get('code')
        email = attrs.get('email')

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise ValidationError('User не существует!')

        cache_key = f"verify_code:{email}"
        # print(cache_key)
        stored_code = cache.get(cache_key)
        # print(f"stored_code = {stored_code}")
        # print(code)

        if stored_code != int(code):
            # print(type(stored_code))
            # print(type(code))
            # print (f"{stored_code} = {code}")
            raise ValidationError("Invalid or expired code")

        cache.delete(cache_key)
        return attrs
    
class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['date-of-birth'] = str(user.dob)
        token['age'] = user.age()
        return token 
    
class GoogleLoginSerializer(serializers.Serializer):
    code = serializers.CharField(required = True)