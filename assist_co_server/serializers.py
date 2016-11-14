from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from rest_framework import serializers, exceptions
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings

from assist_co_server.models import Client, Gender, Profession, TaskType, Task

class GenderField(serializers.RelatedField):
    """
    Custom Gender field 
    """
    def to_representation(self, value):
        return {'permalink': value.permalink, 'sort': value.sort, 'display': value.display}

    def to_internal_value(self, data):
        return Gender.objects.get(permalink=data)

    def get_queryset(self):
        return Gender.objects.all()
        
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

class AssistantSerializer(serializers.ModelSerializer):
    """
    Assistant serializer
    """
    first_name              = serializers.CharField(allow_blank=False, required=True)
    last_name               = serializers.CharField(allow_blank=False, required=True)
    password                = serializers.CharField(allow_blank=False, required=True, write_only=True)
    email                   = serializers.EmailField(max_length=200, allow_blank=False, required=True)
    gender                  = GenderField(many=False)
    date_of_birth           = serializers.DateField(required=True)

    class Meta:
        model = Client
        fields = ('email', 'password','first_name', 'last_name', 'date_of_birth', 'gender')


    def validate_email(self, email):
        try:
            u = User.objects.get(email=email.lower())
            raise exceptions.ValidationError('Email already exists')
        except ObjectDoesNotExist:
            pass
        return email.lower()

class ProfessionField(serializers.RelatedField):
    """
    Custom Profession field 
    """
    def to_representation(self, value):
        return {'permalink': value.permalink, 'sort': value.sort, 'display': value.display}

    def to_internal_value(self, data):
        return Profession.objects.get(permalink=data)

    def get_queryset(self):
        return Profession.objects.all()

class ClientSerializer(serializers.ModelSerializer):
    """
    Client serializer
    """
    first_name              = serializers.CharField(allow_blank=False, required=True)
    last_name               = serializers.CharField(allow_blank=False, required=True)
    password                = serializers.CharField(allow_blank=False, required=True, write_only=True)
    email                   = serializers.EmailField(max_length=200, allow_blank=False, required=True)
    gender                  = GenderField(many=False)
    date_of_birth           = serializers.DateField(required=True)
    phone                   = serializers.CharField(allow_blank=False, required=True)
    profession              = ProfessionField(many=False)
    primary_assistant       = AssistantSerializer(many=False, read_only=True)
    created_on              = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Client
        fields = ('email', 'password','first_name', 'last_name', 'date_of_birth', 
            'date_of_birth', 'gender', 'phone', 'profession', 'primary_assistant',
            'created_on')


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
        fields = ('permalink', 'sort', 'display')

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('permalink', 'sort', 'display')

class TaskTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskType
        fields = ('permalink', 'sort', 'display')

class TaskTypeField(serializers.RelatedField):
    """
    Custom TaskType field 
    """
    def to_representation(self, value):
        return {'permalink': value.permalink, 'sort': value.sort, 'display': value.display}

    def to_internal_value(self, data):
        return TaskType.objects.get(permalink=data)

    def get_queryset(self):
        return TaskType.objects.all()

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task
    """
    task_type = TaskTypeField(many=False)
    client = ClientSerializer(many=False, read_only=True)
    client_id = serializers.SlugRelatedField(many=False, slug_field='id', 
        queryset=Client.objects.all(), write_only=True)
    assistant = AssistantSerializer(many=False, read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'text', 'task_type', 'client', 'client_id', 
            'state','completed_on', 'created_on', 'assistant', 'is_complete')

    def create(self, attrs):
        return Task.objects.create(
            text=attrs['text'], 
            client_id=attrs['client_id'].id, 
            task_type_id=attrs['task_type'].id,
        )
