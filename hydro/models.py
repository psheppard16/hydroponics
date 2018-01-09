from django.db import models
import django.utils.timezone as tz

class Data(models.Model):
    def __str__(self):
        return str(self.type) + ": " + str(self.value) + " on: " + str(self.date_time)

    date_time = models.DateTimeField(null=True)
    type = models.ForeignKey('DataType', null=False, on_delete=True)
    value = models.DecimalField(decimal_places=2, max_digits=5, null=False)

class DataType(models.Model):
    def __str__(self):
        return str(self.type)

    type = models.CharField(max_length=20, null=False)

class RequestType(models.Model):
    def __str__(self):
        return str(self.type)

    type = models.CharField(max_length=20, null=False)

class Status(models.Model):
    def __str__(self):
        return str(self.status)

    status = models.CharField(max_length=20, null=False)

DEFAULT_STATUS_ID = 1
class Request(models.Model):
    def __str__(self):
        return str(self.type) + " on: " + str(self.request_time)

    request_time = models.DateTimeField(null=True, default=tz.now)
    exec_time = models.DateTimeField(null=True)
    type = models.ForeignKey('DataType', null=False, on_delete=True)
    status = models.ForeignKey('Status', default=DEFAULT_STATUS_ID, null=False, on_delete=True)
    value = models.DecimalField(decimal_places=2, max_digits=5, null=True)

class Configuration(models.Model):
    #PH REGULATION
    auto_regulate_pH = models.BooleanField(default=False, null=False)
    low_pH = models.DecimalField(decimal_places=2, max_digits=5, null=False)
    high_pH = models.DecimalField(decimal_places=2, max_digits=5, null=False)
    pH_adj_volume = models.DecimalField(decimal_places=2, max_digits=5, null=False)
    last_pH_change = models.DateTimeField(null=True)

    #NUTRIENT REGULATION
    auto_regulate_nutrients = models.BooleanField(default=False, null=False)
    low_EC = models.DecimalField(decimal_places=2, max_digits=5, null=False)
    high_EC = models.DecimalField(decimal_places=2, max_digits=5, null=False)
    nutrient_adj_volume = models.DecimalField(decimal_places=2, max_digits=5, null=False)
    last_nutrient_change = models.DateTimeField(null=True)

    #WASTE REGULATION
    auto_water_change = models.BooleanField(default=False, null=False)
    low_ORP = models.DecimalField(decimal_places=2, max_digits=5, null=False)
    high_ORP = models.DecimalField(decimal_places=2, max_digits=5, null=False)
    last_water_change = models.DateTimeField(null=True)
    maximum_water_change_interval = models.IntegerField(default=31, null=False) #days
    minimum_water_change_interval = models.IntegerField(default=1, null=False) #days

    #WATER REGULATION
    auto_pump = models.BooleanField(default=False, null=False)
    auto_refill = models.BooleanField(default=False, null=False)
    resevoir_volume = models.IntegerField(default=27, null=False)  # liters
    basin_volume = models.IntegerField(default=27, null=False)  # liters

    #DATA
    min_change_interval = models.IntegerField(default=60, null=False)  # minutes
    polling_range = models.IntegerField(default=60, null=False)  #minutes
    minimun_data_count = models.IntegerField(default=100, null=False)