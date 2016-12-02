from django.utils import timezone

from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.authtoken import views as rest_views
from rest_framework import viewsets, generics, mixins, views, status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response

from assist_co_server import serializers, paginators
from assist_co_server.models import Client, Gender, TaskType, Profession, Task, Assistant, Contact

class LoginView(rest_views.ObtainAuthToken):
    """
    POST
    Log user in by returning their token
    """
    def post(self, request, *args, **kwargs):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            user.last_login = timezone.now()
            user.save()
            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    DELETE
    Delete the users Token
    """
    def delete(self, request, *args, **kwargs):
        token, created = Token.objects.get_or_create(user=request.user)
        token.delete()
        return Response({'success': True})


class ClientSignupView(APIView):
    """
    POST
    Sign the client up and return a valid token for authenticating to server
    """
    def post(self, request, *args, **kwargs):
        serializer = serializers.ClientSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            client = Client.objects.create(
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


class GendersView(generics.ListAPIView):
    """
    GET
    Get all the gender options in db
    """
    queryset = Gender.objects.all()
    serializer_class = serializers.GenderSerializer
    pagination_class = paginators.StandardResultsSetPagination


class TaskTypesView(generics.ListAPIView):
    """
    GET
    Get all the task type options in db
    """
    queryset = TaskType.objects.all()
    serializer_class = serializers.TaskTypeSerializer
    pagination_class = paginators.StandardResultsSetPagination


class ProfessionsView(generics.ListAPIView):
    """
    GET
    Get all the Profession options
    """
    queryset = Profession.objects.all()
    serializer_class = serializers.ProfessionSerializer
    pagination_class = paginators.StandardResultsSetPagination


class TasksView(generics.ListAPIView,
                generics.CreateAPIView):
    """
    GET, POST
    Get all the tasks in db including archived tasks
    """
    queryset = Task.objects.all()
    serializer_class = serializers.TaskSerializer
    pagination_class = paginators.StandardResultsSetPagination


class AssistantsView(generics.ListAPIView,
                    generics.CreateAPIView):

    """
    GET, POST
    List or Create an Assistant. Should only be used by admin not mobile.
    """
    serializer_class = serializers.AssistantSerializer
    pagination_class = paginators.StandardResultsSetPagination
    queryset = Assistant.objects.all()


class AssistantDetailView(generics.RetrieveUpdateAPIView):
    """
    GET, PATCH, DELETE
    Get, update, or delete specified assistant
    """
    serializer_class = serializers.AssistantSerializer

    def get_object(self):
        assistant = get_object_or_404(Assistant, id=self.kwargs['id'])
        return assistant

    def partial_update(self, request, *args, **kwargs):
        """
        PATCH
        Update some or all of the fields for the assistant
        """
        assistant = self.get_object()
        serializer = serializers.AssistantSerializer(assistant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

class ContactsView(generics.CreateAPIView):
    """
    POST
    Create Contact
    """
    serializer_class = serializers.ContactSerializer

class ContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET, PATCH/UPDATE, DELETE
    Contact
    """
    serializer_class = serializers.ContactSerializer
    def get_object(self):
        contact = get_object_or_404(Contact, id=self.kwargs['id'])
        return contact
 
class TaskContactsView(APIView):
    """
    POST
    Add Contacts to task
    """

    def post(self, request, *args, **kwargs):
        """
        Pass in array of Contact json objects create the contacts then add to the Task
        OR
        Pass in array of Contact ids and add the contacts to the Task
        """
        # get the task for this request
        task = get_object_or_404(Task, id=self.kwargs['id'], is_archived=False)
        contact_objs = []
        contacts = request.data['contacts']
        curr_task_contacts = task.contacts
        # check if we have array of objects or ids
        if type(contacts[0]) is dict:
            # We have Contact json objects
            # Create Contact objects if it doesn't already exist
            for contact_attrs in contacts:
                contact = Contact.get_or_create_by_attrs(contact_attrs)
                if curr_task_contacts.filter(id=contact.id).count() == 0:
                    contact_objs.append(contact)
        else:
            # we have contact ids
            contacts_set = Contact.objects.filter(pk__in=contacts)
            if len(contacts) != contacts_set.count():
                return Response("Contact does not exist for one or more IDs provided", status=status.HTTP_400_BAD_REQUEST)
            for contact in contacts_set:
                if curr_task_contacts.filter(id=contact.id).count() == 0:
                    contact_objs.append(contact)

        if len(contact_objs) > 0:
            task.contacts.add(*contact_objs)
            task.save()
        return Response(serializers.TaskSerializer(task).data)

    def get(self, request, *args, **kwargs):
        """
        Get all the contacts for this Task
        """
        task = get_object_or_404(Task, id=self.kwargs['id'], is_archived=False)
        serializer = serializers.ContactSerializer(task.contacts, many=True)
        return Response(serializer.data)

class ClientsView(generics.ListAPIView):
    """
    GET
    Get all the clients in db
    """
    queryset = Client.objects.all()
    serializer_class = serializers.ClientSerializer
    pagination_class = paginators.StandardResultsSetPagination

class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET, PATCH, DELETE
    Get, Patch, DELETE(set to inactive) specific user in db
    """
    serializer_class = serializers.ClientSerializer
    def get_object(self):
        client = get_object_or_404(Client, id=self.kwargs['id'], is_active=True)
        return client

    def partial_update(self, request, *args, **kwargs):
        """
        PATCH
        Update some or all of the fields for the client
        """
        client = self.get_object()
        serializer = serializers.ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        DELETE
        Set Client to inactive
        """
        client = self.get_object()
        client.is_active = False
        client.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ClientTasksView(generics.ListAPIView):
    """
    GET
    List or Create a Task for a specific user
    """
    serializer_class = serializers.TaskSerializer
    pagination_class = paginators.StandardResultsSetPagination

    def get_queryset(self):
        # Return all the tasks that belong to the client
        return Task.objects.filter(client_id=self.kwargs['id'], is_archived=False)

class ClientTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET, PATCH, DELETE
    Get, update, or delete specified task owned by specific client
    """
    serializer_class = serializers.TaskSerializer

    def get_object(self):
        task = get_object_or_404(Task, client_id=self.kwargs['client_id'],
            id=self.kwargs['id'], is_archived=False)
        return task

    def partial_update(self, request, *args, **kwargs):
        """
        PATCH
        Update some or all of the fields for the task
        """
        task = self.get_object()
        serializer = serializers.TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        DELETE
        Set Task to archived
        """
        task = self.get_object()
        task.is_archived = True
        task.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
