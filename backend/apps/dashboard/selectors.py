from apps.results.models import TestResult
from apps.results.selectors import (
    get_latest_result,
    get_previous_results,
    get_biomarker_trend,
)


def get_patient_dashboard(patient, biomarker):
    """
    Fetch all data needed for the patient dashboard.
    Returns a dict with patient, biomarker, latest, previous, history.
    """
    latest = get_latest_result(patient.id, biomarker.id)
    if not latest:
        return None  # No results for this biomarker yet

    previous = get_previous_results(patient.id, biomarker.id, limit=3)
    history = get_biomarker_trend(patient.id, biomarker.id)

    # Compute status for latest
    status = "UNKNOWN"
    if biomarker.reference_min is not None and biomarker.reference_max is not None:
        if biomarker.reference_min <= latest.value <= biomarker.reference_max:
            status = "NORMAL"
        elif latest.value < biomarker.reference_min:
            status = "LOW"
        else:
            status = "HIGH"

    dashboard_data = {
        "patient": patient,
        "biomarker": biomarker,
        "latest": {
            "value": latest.value,
            "unit": latest.unit,
            "test_date": latest.test_date,
            "status": status,
        },
        "previous": [
            {
                "value": r.value,
                "unit": r.unit,
                "test_date": r.test_date,
            }
            for r in previous
        ],
        "history": list(history),  # QuerySet to list for serialization
    }
    return dashboard_data