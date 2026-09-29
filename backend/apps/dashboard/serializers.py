from rest_framework import serializers

from apps.patients.serializers import PatientSerializer
from apps.biomarkers.serializers import BiomarkerSerializer
from apps.results.serializers import TestResultSerializer


class DashboardLatestSerializer(serializers.Serializer):
    """Latest result for a biomarker."""
    value = serializers.DecimalField(max_digits=10, decimal_places=3)
    unit = serializers.CharField()
    test_date = serializers.DateField()
    status = serializers.CharField()


class DashboardPreviousSerializer(serializers.Serializer):
    """Previous results summary."""
    value = serializers.DecimalField(max_digits=10, decimal_places=3)
    unit = serializers.CharField()
    test_date = serializers.DateField()


class DashboardSerializer(serializers.Serializer):
    """Patient dashboard with aggregated data."""
    patient = PatientSerializer()
    biomarker = BiomarkerSerializer()
    latest = DashboardLatestSerializer()
    previous = DashboardPreviousSerializer(many=True)
    change_from_previous = serializers.SerializerMethodField()
    history = TestResultSerializer(many=True)

    def get_change_from_previous(self, obj):
        """Compute latest - previous."""
        if not obj.get("latest") or not obj.get("previous") or not obj["previous"]:
            return None
        latest_value = obj["latest"]["value"]
        previous_value = obj["previous"][0]["value"]
        return float(latest_value - previous_value)