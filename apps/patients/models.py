from datetime import date

from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedModel, UUIDModel


class Patient(UUIDModel, TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"
        OTHER = "O", "Other"

    patient_code = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=Gender.choices)
    medical_history = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="patients_created"
    )

    class Meta:
        ordering = ["patient_code"]
        indexes = [models.Index(fields=["full_name"])]

    @property
    def age(self):
        today = date.today()
        dob = self.date_of_birth
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    def __str__(self):
        return f"{self.patient_code} - {self.full_name}"