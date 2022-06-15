import json

from django.db import models
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from .services import *


class Asset(models.Model):
    class Meta:
        db_table = "asset"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "created_by"], name="unique asset_constraint"
            )
        ]

    PERIOD_CHOICES = [
        ("days", "Days"),
        ("hours", "Hours"),
        ("minutes", "Minutes"),
        ("seconds", "Seconds"),
    ]
    name = models.CharField(max_length=250, blank=True)
    created_by = models.ForeignKey("users.User", on_delete=models.CASCADE)

    # Fields to control sending emails
    min_value = models.DecimalField(max_digits=8, decimal_places=2)
    max_value = models.DecimalField(max_digits=8, decimal_places=2)

    # Fields to control the task periodicity
    period_type = models.CharField(
        choices=PERIOD_CHOICES, max_length=7, default="minutes"
    )
    period_time = models.IntegerField(default=0, blank=True)
    monitoring = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}_{self.created_by.first_name}"
    
    def save(self, *args, **kwargs):
        # Update periodic task only if asset object already exists
        if self.id:
            asset = Asset.objects.get(id=self.id)
            schedule, created = IntervalSchedule.objects.get_or_create(
                period=self.period_type, every=self.period_time
            )
            task = PeriodicTask.objects.get(
                kwargs__contains=json.dumps({
                    "created_by": asset.created_by.id,
                    "asset_name": asset.name
                })
            )
            task.kwargs = json.dumps({
                    "created_by": self.created_by.id,
                    "asset_name": self.name
                })
            task.interval = schedule
            task.enabled = self.monitoring
            task.save()
            if self.name != asset.name:
                AssetData.objects.filter(asset=self).delete()
        else:
            schedule, created = IntervalSchedule.objects.get_or_create(
                period=self.period_type, every=self.period_time
            )
            task_name = f"{self.created_by.email}_{self.name}"
            task = PeriodicTask.objects.create(
                name=task_name,
                interval=schedule,
                task="assets.tasks.get_asset_data",
                kwargs=json.dumps(
                    {"created_by": self.created_by.id, "asset_name": self.name}
                ),
            )
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        PeriodicTask.objects.get(
            kwargs__contains=json.dumps({
                "created_by": self.created_by.id,
                "asset_name": self.name,
            })
        ).delete()
        super().delete(*args, **kwargs)


class AssetData(models.Model):
    asset = models.ForeignKey("assets.Asset", on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=8, decimal_places=2)
    data_extraction_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.asset.monitoring:
            if not self.asset.min_value < self.value < self.asset.max_value:
                send_email(
                    self.asset.name, self.asset.min_value, self.asset.max_value, self.value, self.asset.created_by.id
                )

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.asset.name}_{self.asset.period_time}_{self.asset.period_type}_{self.asset.created_by.first_name}"