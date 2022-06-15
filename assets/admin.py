from django.contrib import admin
from django.contrib.auth.models import Group

from django_celery_beat.models import (
    IntervalSchedule,
    SolarSchedule,
    CrontabSchedule,
    ClockedSchedule,
    PeriodicTask,
)

from .models import Asset, AssetData


class AssetAdmin(admin.ModelAdmin):
    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


class AssetDataAdmin(admin.ModelAdmin):
    readonly_fields = ["asset", "value"]


admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetData, AssetDataAdmin)

# Hide admin of unnecessary models
admin.site.unregister(Group)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(PeriodicTask)
