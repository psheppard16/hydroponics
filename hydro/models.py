from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings

# @receiver(post_save, sender=Model, dispatch_uid="model_postsave")
# def model_postsave(sender, instance, created, **kwargs):
# 	pass
#
#
# class Model(models.Model):
# 	pass

class Data(models.Model):
    date_time = models.DateTimeField(null=True)
    type = models.ForeignKey('Type', null=False, on_delete=True)
    value = models.DecimalField(decimal_places=2, max_digits=5, null=False)

class Type(models.Model):
    type = models.CharField(max_length=20, null=False)