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
    phone = PhoneNumberField(blank=True, null=True, unique=True)
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

class Task(models.Model):
    class Meta:
        db_table = 'tasks'
    client = models.ForeignKey(Client)
    assistant = models.ForeignKey(Assistant, null=True)
    text = models.TextField()
    task_type = models.ForeignKey(TaskType, null=False)
    state = models.CharField(choices=TASK_STATES, default='ready', max_length=100)
    is_complete = models.BooleanField(default=False) 
    is_archived = models.BooleanField(default=False)
    completed_on = models.DateTimeField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
