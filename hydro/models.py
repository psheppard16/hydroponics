from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings

# @receiver(post_save, sender=Model, dispatch_uid="model_postsave")
# def model_postsave(sender, instance, created, **kwargs):
# 	pass

class Data(models.Model):
    date_time = models.DateTimeField(null=True)
    type = models.ForeignKey('Type', null=False, on_delete=True)
    value = models.DecimalField(decimal_places=2, max_digits=5, null=False)

class Type(models.Model):
    type = models.CharField(max_length=20, null=False)

class Configuration(models.Model):
    #REGULATION
    auto_regulate = models.BooleanField(default=False, null=False)
    min_change_interval = models.IntegerField(default=60, null=False) #seconds
    polling_range = models.IntegerField(default=60, null=False) #seconds
    minimun_data_count = models.IntegerField(default=100, null=False)

    low_pH = models.DecimalField(decimal_places=2, max_digits=5, null=False)
    high_pH = models.DecimalField(decimal_places=2, max_digits=5, null=False)
    pH_adj_volume = models.DecimalField(decimal_places=2, max_digits=5, null=False)
    last_pH_change = models.DateTimeField(null=True)

    low_EC = models.DecimalField(decimal_places=2, max_digits=5, null=False)
    high_EC = models.DecimalField(decimal_places=2, max_digits=5, null=False)
    nutrient_adj_volume = models.DecimalField(decimal_places=2, max_digits=5, null=False)
    last_nutrient_change = models.DateTimeField(null=True)

    #WATER CHANGE
    auto_water_change = models.BooleanField(default=False, null=False)
    low_ORP = models.DecimalField(decimal_places=2, max_digits=5, null=False)
    high_ORP = models.DecimalField(decimal_places=2, max_digits=5, null=False)
    last_water_change = models.DateTimeField(null=True)
    maximum_water_change_interval = models.IntegerField(default=31, null=False) #days
    minimum_water_change_interval = models.IntegerField(default=1, null=False) #days

    #PUMPING
    auto_pump = models.BooleanField(default=False, null=False)

    #REFILL
    auto_refill = models.BooleanField(default=False, null=False)

    resevoir_volume = models.IntegerField(default=27, null=False) #Liters
    basin_volume = models.IntegerField(default=27, null=False) #Liters