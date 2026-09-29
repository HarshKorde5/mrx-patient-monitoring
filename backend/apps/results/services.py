from datetime import date

from django.db import transaction
from rest_framework.exceptions import ValidationError

from .models import TestResult


@transaction.atomic
def create_test_result(
    *, patient, biomarker, value, test_date, recorded_by, notes=""
) -> TestResult:
    """Create a result with validation."""
    
    # Validate value
    if value < 0:
        raise ValidationError({"value": "Value cannot be negative."})

    # Validate date
    if test_date > date.today():
        raise ValidationError({"test_date": "Test date cannot be in the future."})

    if patient.date_of_birth and test_date < patient.date_of_birth:
        raise ValidationError(
            {"test_date": "Test date cannot be before patient's date of birth."}
        )

    result = TestResult.objects.create(
        patient=patient,
        biomarker=biomarker,
        value=value,
        unit=biomarker.unit,  # snapshot the unit
        test_date=test_date,
        notes=notes,
        recorded_by=recorded_by,
    )
    return result