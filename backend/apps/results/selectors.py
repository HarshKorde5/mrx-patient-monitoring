from django.db.models import QuerySet

from .models import TestResult


def get_patient_results(patient_id) -> QuerySet:
    """All results for a patient, ordered by date."""
    return (
        TestResult.objects.filter(patient_id=patient_id)
        .select_related("biomarker", "recorded_by")
        .order_by("-test_date", "-created_at")
    )


def get_biomarker_trend(patient_id, biomarker_id) -> QuerySet:
    """Time series for a biomarker on a patient."""
    return (
        TestResult.objects.filter(patient_id=patient_id, biomarker_id=biomarker_id)
        .select_related("biomarker")
        .only("id", "value", "unit", "test_date", "biomarker__name", "biomarker__unit")
        .order_by("test_date")
    )


def get_latest_result(patient_id, biomarker_id) -> TestResult:
    """Most recent result for a biomarker on a patient."""
    return (
        TestResult.objects.filter(patient_id=patient_id, biomarker_id=biomarker_id)
        .select_related("biomarker")
        .order_by("-test_date")
        .first()
    )


def get_previous_results(patient_id, biomarker_id, limit=3) -> QuerySet:
    """Previous results before latest, for dashboard."""
    return (
        TestResult.objects.filter(patient_id=patient_id, biomarker_id=biomarker_id)
        .select_related("biomarker")
        .order_by("-test_date")[1 : limit + 1]
    )