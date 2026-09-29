from rest_framework import viewsets, permissions

from apps.common.permissions import IsAdmin
from .models import Biomarker
from .serializers import BiomarkerSerializer, BiomarkerCreateUpdateSerializer


class BiomarkerViewSet(viewsets.ModelViewSet):
    queryset = Biomarker.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["name", "code"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return BiomarkerCreateUpdateSerializer
        return BiomarkerSerializer

    def get_permissions(self):
        """Only Admin can create/update/delete biomarkers."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]