from django.contrib import admin
from hydro.models import *
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin


class DataAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ("type", "value", "date_time")
    filter_horizontal = ()
    search_fields = ["date_time", "type", "value"]
    fields = ("date_time", "type", "value")
    readonly_fields = ()
    list_filter = []


admin.site.register(Data, DataAdmin)


class WasteSettingsAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ("id",)
    filter_horizontal = ()
    search_fields = []
    fields = ()
    readonly_fields = ()
    list_filter = []


admin.site.register(WasteSettings, WasteSettingsAdmin)


class ChemicalSettingsAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ("id",)
    filter_horizontal = ()
    search_fields = []
    fields = ()
    readonly_fields = ()
    list_filter = []


admin.site.register(ChemicalSettings, ChemicalSettingsAdmin)


class RequestAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ("type", "status")
    filter_horizontal = ()
    search_fields = ["request_time", "type", "arg1", "arg2", "status"]
    fields = ("request_time", "exec_time", "type", "arg1", "arg2", "status")
    readonly_fields = ()
    list_filter = []


admin.site.register(Request, RequestAdmin)


class DataTypeAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ("type",)
    filter_horizontal = ()
    search_fields = ["type"]
    fields = ("type",)
    readonly_fields = ()
    list_filter = ["type"]


admin.site.register(DataType, DataTypeAdmin)


class RequestTypeAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ("type",)
    filter_horizontal = ()
    search_fields = ["type"]
    fields = ("type",)
    readonly_fields = ()
    list_filter = ["type"]


admin.site.register(RequestType, RequestTypeAdmin)


class StatusAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ("status",)
    filter_horizontal = ()
    search_fields = ["status"]
    fields = ("status",)
    readonly_fields = ()
    list_filter = ["status"]


admin.site.register(Status, StatusAdmin)
