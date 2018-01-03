from django.contrib import admin
from hydro.models import *
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

# class ModelAdmin(SimpleHistoryAdmin, ImportExportModelAdmin, ImportExportActionModelAdmin):
# 	list_display = ()
# 	filter_horizontal = ()
# 	search_fields = []
# 	fields = ()
# 	readonly_fields = ()
# 	list_filter = []

# admin.site.register(Model, ModelAdmin)
