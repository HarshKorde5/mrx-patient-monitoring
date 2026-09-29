from django.db import models

from apps.common.models import TimeStampedModel, UUIDModel


class Biomarker(UUIDModel, TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=30, unique=True)
    unit = models.CharField(max_length=20)
    reference_min = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    reference_max = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.unit})"