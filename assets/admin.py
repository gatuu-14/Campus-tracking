from django.contrib import admin
from .models import Department, AssetCategory, Asset, AssetMovement, MaintenanceRecord


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'head_of_department')
    search_fields = ('name', 'head_of_department')


@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'department', 'condition', 'status', 'purchase_date')
    list_filter = ('category', 'department', 'status', 'condition')
    search_fields = ('name', 'serial_number')
    ordering = ('-date_added',)


@admin.register(AssetMovement)
class AssetMovementAdmin(admin.ModelAdmin):
    list_display = ('asset', 'from_department', 'to_department', 'moved_by', 'date_moved')
    list_filter = ('from_department', 'to_department')
    search_fields = ('asset__name', 'moved_by__username')


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ('asset', 'issue_reported', 'maintenance_date', 'performed_by')
    list_filter = ('maintenance_date',)
    search_fields = ('asset__name', 'performed_by')
    date_hierarchy = ('maintenance_date')

