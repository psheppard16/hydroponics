from django.db import models
import django.utils.timezone as tz


class Data(models.Model):
    def __str__(self):
        return str(self.type) + ": " + str(self.value) + " on: " + str(self.date_time)

    date_time = models.DateTimeField(blank=False)
    type = models.ForeignKey('DataType', blank=False, on_delete=True)
    value = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)


class DataType(models.Model):
    def __str__(self):
        return str(self.type)

    type = models.CharField(max_length=20, blank=False)


class RequestType(models.Model):
    def __str__(self):
        return str(self.type)

    type = models.CharField(max_length=20, blank=False)


class Status(models.Model):
    def __str__(self):
        return str(self.status)

    status = models.CharField(max_length=20, blank=False)


DEFAULT_STATUS_ID = 1


class Request(models.Model):
    def __str__(self):
        return str(self.type) + " on: " + str(self.request_time)

    request_time = models.DateTimeField(blank=True, default=tz.now)
    exec_time = models.DateTimeField(blank=True, null=True)
    type = models.ForeignKey('RequestType', blank=False, on_delete=True)
    status = models.ForeignKey('Status', default=DEFAULT_STATUS_ID, blank=False, on_delete=True)
    arg1 = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
    arg2 = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)


class ChemicalSettings(models.Model):
    # PH REGULATION
    auto_regulate_pH = models.BooleanField(default=False, blank=False)
    low_pH = models.DecimalField(decimal_places=2, max_digits=5, blank=False)
    high_pH = models.DecimalField(decimal_places=2, max_digits=5, blank=False)
    pH_adj_volume = models.DecimalField(decimal_places=2, max_digits=5, blank=False)
    last_pH_change = models.DateTimeField(null=True, blank=True)

    # NUTRIENT REGULATION
    auto_regulate_nutrients = models.BooleanField(default=False, blank=False)
    low_EC = models.DecimalField(decimal_places=2, max_digits=5, blank=False)
    high_EC = models.DecimalField(decimal_places=2, max_digits=5, blank=False)
    nutrient_adj_volume = models.DecimalField(decimal_places=2, max_digits=5, blank=False)
    last_nutrient_change = models.DateTimeField(null=True, blank=True)

    # ORP REGULATION
    auto_regulate_ORP = models.BooleanField(default=False, blank=False)
    low_ORP = models.DecimalField(decimal_places=2, max_digits=5, blank=False)
    high_ORP = models.DecimalField(decimal_places=2, max_digits=5, blank=False)
    ORP_adj_volume = models.DecimalField(decimal_places=2, max_digits=5, blank=False)
    last_ORP_change = models.DateTimeField(null=True, blank=True)

    # DATA
    min_change_interval = models.IntegerField(default=60, blank=False)  # minutes
    polling_range = models.IntegerField(default=60, blank=False)  # minutes
    minimun_data_count = models.IntegerField(default=100, blank=False)


class WasteSettings(models.Model):
    # WASTE REGULATION
    auto_water_change = models.BooleanField(default=False, blank=False)
    last_water_change = models.DateTimeField(null=True, blank=True)
    maximum_water_change_interval = models.IntegerField(default=31, blank=False)  # days
    minimum_water_change_interval = models.IntegerField(default=1, blank=False)  # days

    # WATER REGULATION
    auto_pump = models.BooleanField(default=False, blank=False)
    auto_refill = models.BooleanField(default=False, blank=False)
    resevoir_volume = models.IntegerField(default=27, blank=False)  # liters
    basin_volume = models.IntegerField(default=27, blank=False)  # liters
