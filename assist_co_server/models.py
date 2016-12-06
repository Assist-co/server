from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, UserManager
from django.dispatch import receiver

from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.authtoken.models import Token

TASK_STATES = (('ready','ready'), 
    ('executing','executing'), 
    ('completed','completed'), 
    ('terminated','terminated'))

### Constants ###

class TaskType(models.Model):
    class Meta:
        db_table = 'task_types'

    sort                = models.SmallIntegerField()
    display             = models.CharField(max_length=100)
    permalink           = models.CharField(db_index=True, max_length=100)

    def __unicode__(self):
        return '%s' % (self.display)

class Profession(models.Model):
    class Meta:
        db_table = 'professions'

    sort                = models.SmallIntegerField()
    display             = models.CharField(max_length=100)
    permalink           = models.CharField(db_index=True, max_length=100)

    def __unicode__(self):
        return '%s' % (self.display)

class Gender(models.Model):
    class Meta:
        db_table = 'genders'

    sort                = models.SmallIntegerField()
    display             = models.CharField(max_length=10)
    permalink           = models.CharField(db_index=True, max_length=10)

    def __unicode__(self):
        return '%s' % (self.display)

### Models ###

def upload_to(instance, filename):
    return 'user_profile_image/{}/{}'.format(instance.user_id, filename)

class Assistant(User):
    class Meta:
        db_table = 'assistants'
    gender = models.ForeignKey(Gender)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    profile_pic = models.ImageField(blank=True, null=True, upload_to=upload_to)
    date_of_birth = models.DateField(null=False)
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

class Client(User):
    class Meta:
        db_table = 'clients'
    primary_assistant = models.ForeignKey(Assistant, null=True)
    phone = models.CharField(max_length=30, null=True)
    profession = models.ForeignKey(Profession)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    profile_pic = models.ImageField(blank=True, null=True, upload_to=upload_to)
    date_of_birth = models.DateField(null=False)
    gender = models.ForeignKey(Gender, null=False)
    # Use UserManager to get the create_user method, etc.
    objects = UserManager()

    def __unicode__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_or_create_token(self):
        """
        Get or create the token associated with the user
        """
        return Token.objects.get_or_create(user=self.user_ptr)[0]

class Contact(models.Model):
    class Meta:
        db_table = 'contacts'
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(Client, null=True, default=None)

    @classmethod
    def get_or_create_by_attrs(self, contact_attrs):
        """
        Create contact object if it doesn't already exist
        """
        if contact_attrs['email']:
            try:
                contact = self.objects.get(email=contact_attrs['email'], client_id=contact_attrs['client_id'])
                return contact
            except :
                # create contact
                return self.objects.create(**contact_attrs)
        else:
            try:
                contact = self.objects.get(phone=contact_attrs['phone'], client_id=contact_attrs['client_id'])
                return contact
            except:
                # create contact
                return self.objects.create(**contact_attrs)

class Task(models.Model):
    class Meta:
        db_table = 'tasks'
    client = models.ForeignKey(Client)
    assistant = models.ForeignKey(Assistant, null=True)
    text = models.TextField()
    location = models.CharField(null=True, max_length=30) # (40.76,-73.984)
    contacts = models.ManyToManyField(Contact)
    task_type = models.ForeignKey(TaskType, null=False)
    state = models.CharField(choices=TASK_STATES, default='ready', max_length=100)
    is_complete = models.BooleanField(default=False) 
    is_archived = models.BooleanField(default=False)
    start_on = models.DateTimeField(null=True)
    end_on = models.DateTimeField(null=True)
    completed_on = models.DateTimeField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
