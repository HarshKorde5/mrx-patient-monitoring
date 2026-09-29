from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.patients.models import Patient
from apps.biomarkers.models import Biomarker
from .serializers import DashboardSerializer
from .selectors import get_patient_dashboard


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def patient_dashboard(request, patient_id):
    """
    GET /api/v1/dashboard/patient/<patient_id>/?biomarker_id=<biomarker_id>
    
    Returns aggregated dashboard data for a patient and biomarker.
    If biomarker_id is not specified, uses the first biomarker with results.
    """
    try:
        patient = Patient.objects.get(id=patient_id, is_active=True)
    except Patient.DoesNotExist:
        return Response(
            {"error": "Patient not found or inactive"},
            status=status.HTTP_404_NOT_FOUND,
        )

    biomarker_id = request.query_params.get("biomarker_id")

    if biomarker_id:
        try:
            biomarker = Biomarker.objects.get(id=biomarker_id, is_active=True)
        except Biomarker.DoesNotExist:
            return Response(
                {"error": "Biomarker not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
    else:
        # Get first biomarker that has results for this patient
        from apps.results.models import TestResult
        result = (
            TestResult.objects.filter(patient=patient)
            .select_related("biomarker")
            .order_by("-test_date")
            .first()
        )
        if not result:
            return Response(
                {"error": "No test results for this patient yet"},
                status=status.HTTP_404_NOT_FOUND,
            )
        biomarker = result.biomarker

    dashboard = get_patient_dashboard(patient, biomarker)
    if not dashboard:
        return Response(
            {"error": "No results for this biomarker"},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = DashboardSerializer(dashboard)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def patient_biomarkers(request, patient_id):
    """
    GET /api/v1/dashboard/patient/<patient_id>/biomarkers/
    
    List all biomarkers that have results for a patient.
    """
    try:
        patient = Patient.objects.get(id=patient_id, is_active=True)
    except Patient.DoesNotExist:
        return Response(
            {"error": "Patient not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    from apps.results.models import TestResult
    biomarkers = (
        Biomarker.objects.filter(
            id__in=TestResult.objects.filter(patient=patient).values_list(
                "biomarker_id", flat=True
            )
        )
        .filter(is_active=True)
        .order_by("name")
    )

    from apps.biomarkers.serializers import BiomarkerSerializer
    serializer = BiomarkerSerializer(biomarkers, many=True)
    return Response(serializer.data)