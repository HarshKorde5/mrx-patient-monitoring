from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.common.permissions import IsDoctorOrAdmin
from apps.patients.models import Patient
from apps.biomarkers.models import Biomarker
from apps.results.selectors import get_biomarker_trend
from apps.reports.serializers import ReportSerializer
from . import services


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def report_data(request, patient_id):
    """
    GET /api/v1/reports/patient/<patient_id>/?biomarker_id=<biomarker_id>
    
    Returns report data as JSON (patient, biomarker, results).
    """
    try:
        patient = Patient.objects.get(id=patient_id, is_active=True)
    except Patient.DoesNotExist:
        return Response(
            {"error": "Patient not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    biomarker_id = request.query_params.get("biomarker_id")
    if not biomarker_id:
        return Response(
            {"error": "biomarker_id query param required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        biomarker = Biomarker.objects.get(id=biomarker_id, is_active=True)
    except Biomarker.DoesNotExist:
        return Response(
            {"error": "Biomarker not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    results = list(get_biomarker_trend(patient_id, biomarker_id))

    from django.utils import timezone
    report_data_dict = {
        "patient": patient,
        "biomarker": biomarker,
        "history": results,
        "generated_at": timezone.now(),
        "generated_by": request.user.username,
    }

    serializer = ReportSerializer(report_data_dict)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsDoctorOrAdmin])
def report_pdf(request, patient_id):
    """
    GET /api/v1/reports/patient/<patient_id>/pdf/?biomarker_id=<biomarker_id>
    
    Returns PDF file download.
    Doctor/Admin only.
    """
    try:
        patient = Patient.objects.get(id=patient_id, is_active=True)
    except Patient.DoesNotExist:
        return Response(
            {"error": "Patient not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    biomarker_id = request.query_params.get("biomarker_id")
    if not biomarker_id:
        return Response(
            {"error": "biomarker_id query param required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        biomarker = Biomarker.objects.get(id=biomarker_id, is_active=True)
    except Biomarker.DoesNotExist:
        return Response(
            {"error": "Biomarker not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    results = list(get_biomarker_trend(patient_id, biomarker_id))
    if not results:
        return Response(
            {"error": "No results for this biomarker"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Generate PDF
    pdf_bytes = services.generate_report_pdf(patient, biomarker, results, request.user)

    # Return PDF response
    from django.http import HttpResponse
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="report_{patient.patient_code}_{biomarker.code}.pdf"'
    return response