from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.common.permissions import IsDoctorOrAdmin, IsAdmin
from .models import Patient
from .serializers import PatientSerializer, PatientCreateUpdateSerializer
from .filters import PatientFilter
from . import services


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]
    filterset_class = PatientFilter
    search_fields = ["patient_code", "full_name"]
    ordering_fields = ["patient_code", "full_name", "created_at"]
    ordering = ["patient_code"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return PatientCreateUpdateSerializer
        return PatientSerializer

    def get_permissions(self):
        """Restrict create/update to Doctor/Admin, delete to Admin only."""
        if self.action in ["create", "update", "partial_update"]:
            permission_classes = [IsDoctorOrAdmin]
        elif self.action == "destroy":
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[IsAdmin])
    def deactivate(self, request, pk=None):
        """Soft delete endpoint: mark patient inactive."""
        patient = self.get_object()
        services.deactivate_patient(patient=patient)
        return Response({"message": "Patient deactivated."})