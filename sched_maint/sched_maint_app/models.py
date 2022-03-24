from tkinter import CASCADE
from django.db import models

class Instance(models.Model):
    maintenance = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.maintenance

class Timing(models.Model):
    interval = models.IntegerField(error_messages={'required': 'Required'})
    instance = models.ForeignKey(Instance, related_name="maint_ints", on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.interval

# Create your models here.