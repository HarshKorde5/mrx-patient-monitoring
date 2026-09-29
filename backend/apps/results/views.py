from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.permissions import IsDoctorOrAdmin
from apps.patients.models import Patient
from apps.biomarkers.models import Biomarker
from .models import TestResult
from .serializers import TestResultSerializer, TestResultCreateSerializer
from .selectors import get_patient_results, get_biomarker_trend, get_latest_result, get_previous_results
from . import services


class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    ordering_fields = ["test_date", "created_at"]
    ordering = ["-test_date"]

    def get_serializer_class(self):
        if self.action == "create":
            return TestResultCreateSerializer
        return TestResultSerializer

    def get_permissions(self):
        """Only Doctor/Admin can create; all auth can read."""
        if self.action == "create":
            permission_classes = [IsDoctorOrAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def by_patient(self, request):
        """Get all results for a patient: /results/by_patient/?patient_id=<id>"""
        patient_id = request.query_params.get("patient_id")
        if not patient_id:
            return Response(
                {"error": "patient_id query param required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return Response(
                {"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND
            )

        results = get_patient_results(patient_id)
        serializer = TestResultSerializer(results, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def trend(self, request):
        """Get trend for a biomarker: /results/trend/?patient_id=<id>&biomarker_id=<id>"""
        patient_id = request.query_params.get("patient_id")
        biomarker_id = request.query_params.get("biomarker_id")

        if not patient_id or not biomarker_id:
            return Response(
                {"error": "patient_id and biomarker_id query params required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            Patient.objects.get(id=patient_id)
            Biomarker.objects.get(id=biomarker_id)
        except (Patient.DoesNotExist, Biomarker.DoesNotExist):
            return Response(
                {"error": "Patient or Biomarker not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        results = get_biomarker_trend(patient_id, biomarker_id)
        serializer = TestResultSerializer(results, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        patient_id = serializer.validated_data["patient"].id
        biomarker_id = serializer.validated_data["biomarker"].id
        value = serializer.validated_data["value"]
        test_date = serializer.validated_data["test_date"]
        notes = serializer.validated_data.get("notes", "")

        patient = Patient.objects.get(id=patient_id)
        biomarker = Biomarker.objects.get(id=biomarker_id)

        result = services.create_test_result(
            patient=patient,
            biomarker=biomarker,
            value=value,
            test_date=test_date,
            notes=notes,
            recorded_by=self.request.user,
        )
        return result