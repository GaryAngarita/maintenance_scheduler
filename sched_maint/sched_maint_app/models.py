from operator import mod
from tkinter import CASCADE
import re
import bcrypt
from django.db import models

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        user_emails = User.objects.filter(email = postData['email'])
        if len(postData['first_name']) == 0:
            errors['blank_first'] = 'First name cannot be blank'
        if len(postData['last_name']) == 0:
            errors['blank_last'] = 'Last name cannot be blank'
        if len(postData['first_name']) < 2:
            errors['short_first'] = 'First name must be more than 2 letters'
        if len(postData['last_name']) < 2:
            errors['short_last'] = 'Last name must be greater than 2 letters'
        if len(postData['email']) == 0:
            errors['miss_email'] = 'Email cannot be blank'
        if not email_regex.match(postData['email']):
            errors['invalid_email'] = 'Not a valid email address'
        if user_emails:
            errors['email_exists'] = 'Email already in use'
        if len(postData['password']) == 0:
            errors['blank_pass'] = 'Password is required'
        if len(postData['password']) < 6:
            errors['short_pass'] = 'Password must be greater than 6 characters'
        if postData['password'] != postData['pw_conf']:
            errors['confirm'] = 'Passwords do not match'
        return errors

    def log_validator(self, postData):
        errors = {}
        user_emails = User.objects.filter(email = postData['email'])
        if not email_regex.match(postData['email']):
            errors['invalid_email'] = 'Invalid email address'
        if not user_emails:
            errors['nonexistent'] = 'Email does not exist'
        if len(postData['password']) < 6:
            errors['short_pass'] = 'Password must be greater than 6 characters'
        if bcrypt.checkpw(postData['password'].encode(), user_emails[0].password.encode()):
            print('password matches')
        else:
            errors['bad_pass'] = 'Email and password do not match'
        return errors

class User(models.Model):
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        email = models.EmailField(max_length=255)
        password = models.CharField(max_length=255)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)
        objects = UserManager()

        def __str__(self):
            return self.first_name, self.last_name
        

class Instance(models.Model):
    user = models.ForeignKey(User, related_name='user_insts', on_delete=CASCADE)
    owner = models.CharField(max_length=255, blank=False, null=False)
    maintenance = models.CharField(max_length=255)
    interval = models.IntegerField(error_messages={'required': 'Required'}, blank=False)
    date_due = models.DateField(blank=False)
    status = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Instance({self.maintenance},{self.interval})'
# Create your models here.