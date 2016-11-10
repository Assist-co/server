from django.utils import timezone

from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import Http404

from rest_framework.authtoken import views as rest_views
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from assist_co_server import serializers
from assist_co_server.models import Client

class LoginView(rest_views.ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            user.last_login = timezone.now()
            user.save()
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

class LogoutView(APIView):
    def delete(self, request, *args, **kwargs):
        token, created = Token.objects.get_or_create(user=request.user)
        token.delete()
        return Response({'success': True})

class ClientSignupView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = serializers.ClientSignupSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            client = models.Client.objects.create(
                username=data['email'],
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                phone=data['phone'],
                profession=data['profession'],
                gender=data['gender'],
                date_of_birth=data['date_of_birth']
            )
            token = client.get_or_create_token()
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
