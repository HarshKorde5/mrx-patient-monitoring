from django.conf import settings
from django.db import models

from apps.common.models import TimeStampedModel, UUIDModel


class TestResult(UUIDModel, TimeStampedModel):
    patient = models.ForeignKey(
        "patients.Patient", on_delete=models.PROTECT, related_name="results"
    )
    biomarker = models.ForeignKey(
        "biomarkers.Biomarker", on_delete=models.PROTECT, related_name="results"
    )
    value = models.DecimalField(max_digits=10, decimal_places=3)
    unit = models.CharField(max_length=20)
    test_date = models.DateField()
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="results_recorded"
    )

    class Meta:
        ordering = ["-test_date", "-created_at"]
        indexes = [models.Index(fields=["patient", "biomarker", "test_date"])]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(value__gte=0), name="result_value_non_negative"
            ),
        ]

    def __str__(self):
        return f"{self.patient.patient_code} | {self.biomarker.code} = {self.value} on {self.test_date}"