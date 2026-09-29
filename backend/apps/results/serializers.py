from datetime import date

from rest_framework import serializers

from apps.patients.serializers import PatientSerializer
from apps.biomarkers.serializers import BiomarkerSerializer
from .models import TestResult


class TestResultSerializer(serializers.ModelSerializer):
    patient_code = serializers.CharField(source="patient.patient_code", read_only=True)
    biomarker_name = serializers.CharField(source="biomarker.name", read_only=True)
    recorded_by_username = serializers.CharField(
        source="recorded_by.username", read_only=True
    )
    status = serializers.SerializerMethodField()

    class Meta:
        model = TestResult
        fields = [
            "id",
            "patient",
            "patient_code",
            "biomarker",
            "biomarker_name",
            "value",
            "unit",
            "test_date",
            "notes",
            "status",
            "recorded_by",
            "recorded_by_username",
            "created_at",
        ]
        read_only_fields = ["id", "unit", "recorded_by", "created_at", "status"]

    def get_status(self, obj):
        """Compute status based on reference range."""
        if not obj.biomarker.reference_min or not obj.biomarker.reference_max:
            return "UNKNOWN"
        if obj.biomarker.reference_min <= obj.value <= obj.biomarker.reference_max:
            return "NORMAL"
        elif obj.value < obj.biomarker.reference_min:
            return "LOW"
        else:
            return "HIGH"


class TestResultCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ["patient", "biomarker", "value", "test_date", "notes"]

    def validate_value(self, value):
        if value < 0:
            raise serializers.ValidationError("Value cannot be negative.")
        return value

    def validate_test_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Test date cannot be in the future.")
        return value

    def validate(self, data):
        patient = data.get("patient")
        test_date = data.get("test_date")

        if patient.date_of_birth and test_date < patient.date_of_birth:
            raise serializers.ValidationError(
                {"test_date": "Test date cannot be before patient's date of birth."}
            )
        return data