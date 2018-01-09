from django.contrib import admin
from hydro.models import *
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

class DataAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
	list_display = ()
	filter_horizontal = ()
	search_fields = ["date_time", "type", "value"]
	fields = ("date_time", "type", "value")
	readonly_fields = ()
	list_filter = []
admin.site.register(Data, DataAdmin)

class ConfigurationAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
	list_display = ()
	filter_horizontal = ()
	search_fields = []
	fields = ("auto_regulate_pH", "auto_regulate_nutrients", "min_change_interval", "polling_range", "minimun_data_count",
        "low_pH", "high_pH", "pH_adj_volume", "last_pH_change", "low_EC", "high_EC",
        "nutrient_adj_volume", "last_nutrient_change", "auto_water_change", "low_ORP", "high_ORP",
        "last_water_change", "maximum_water_change_interval", "minimum_water_change_interval", "auto_pump",
		"auto_refill", "resevoir_volume", "basin_volume")
	readonly_fields = ()
	list_filter = []
admin.site.register(Configuration, ConfigurationAdmin)

class RequestAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
	list_display = ()
	filter_horizontal = ()
	search_fields = ["request_time", "type", "value", "status"]
	fields = ("request_time", "exec_time", "type", "value", "status")
	readonly_fields = ()
	list_filter = []
admin.site.register(Request, RequestAdmin)

class DataTypeAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
	list_display = ()
	filter_horizontal = ()
	search_fields = ["type"]
	fields = ("type",)
	readonly_fields = ()
	list_filter = ["type"]
admin.site.register(DataType, DataTypeAdmin)

class RequestTypeAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
	list_display = ()
	filter_horizontal = ()
	search_fields = ["type"]
	fields = ("type",)
	readonly_fields = ()
	list_filter = ["type"]
admin.site.register(RequestType, RequestTypeAdmin)

class StatusAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
	list_display = ()
	filter_horizontal = ()
	search_fields = ["status"]
	fields = ("status",)
	readonly_fields = ()
	list_filter = ["status"]
admin.site.register(Status, StatusAdmin)