from rest_framework import serializers

from apps.patients.serializers import PatientSerializer
from apps.biomarkers.serializers import BiomarkerSerializer
from apps.results.serializers import TestResultSerializer


class ReportSerializer(serializers.Serializer):
    """Report data structure."""
    patient = PatientSerializer()
    biomarker = BiomarkerSerializer()
    history = TestResultSerializer(many=True)
    generated_at = serializers.DateTimeField()
    generated_by = serializers.CharField()