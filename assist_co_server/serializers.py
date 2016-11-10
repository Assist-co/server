from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings

from assist_co_server.models import Client, Gender, Profession, TaskType

class LoginSerializer(serializers.Serializer):
    """
    Login client serializer
    """
    email = serializers.EmailField(allow_blank=False, required=True)
    password = serializers.CharField(allow_blank=False, required=True)

    def validate(self, attrs):
        email = attrs['email']
        password = attrs['password']
        user = None

        if email and password:
            email = email.lower()
            user = authenticate(email=email, password=password)
        else:
            raise exceptions.ValidationError('Must include "email" and "password".')

        # Did we get back an active user?
        if user:
            if not user.is_active:
                raise exceptions.ValidationError('User account is disabled.')
        else:
            raise exceptions.ValidationError('Unable to log in with provided credentials.')

        attrs['user'] = user
        return attrs

class ClientSignupSerializer(serializers.ModelSerializer):
    """
    Register client serializer
    """
    first_name              = serializers.CharField(allow_blank=False, required=True)
    last_name               = serializers.CharField(allow_blank=False, required=True)
    password                = serializers.CharField(allow_blank=False, required=True, write_only=True)
    email                   = serializers.EmailField(max_length=200, allow_blank=False, required=True)
    gender                  = serializers.SlugRelatedField(many=False, slug_field='permalink', queryset=Gender.objects.all())
    date_of_birth           = serializers.DateField(required=True)
    phone                   = serializers.CharField(allow_blank=False, required=True)
    profession              = serializers.SlugRelatedField(many=False, slug_field='permalink', queryset=Profession.objects.all())

    class Meta:
        model = Client
        fields = ('email', 'password','first_name', 'last_name', 'date_of_birth', 
            'date_of_birth', 'gender', 'phone', 'profession')


    def validate_email(self, email):
        try:
            u = User.objects.get(email=email.lower())
            raise exceptions.ValidationError('Email already exists')
        except ObjectDoesNotExist:
            pass
        return email.lower()

    def validate_phone(self, phone):
        try:
            u = Client.objects.get(phone=phone)
            raise exceptions.ValidationError('Phone number already exists')
        except ObjectDoesNotExist:
            pass
        return phone

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ('permalink', 'option_id', 'display')

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('permalink', 'option_id', 'display')
        
class TaskTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskType
        fields = ('permalink', 'option_id', 'display')