from rest_framework import serializers

from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    created_by_username = serializers.CharField(source="created_by.username", read_only=True)

    class Meta:
        model = Patient
        fields = [
            "id",
            "patient_code",
            "full_name",
            "date_of_birth",
            "age",
            "gender",
            "medical_history",
            "is_active",
            "created_by",
            "created_by_username",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]

    def get_age(self, obj):
        return obj.age


class PatientCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["patient_code", "full_name", "date_of_birth", "gender", "medical_history"]

    def validate_patient_code(self, value):
        if self.instance:  # editing
            if Patient.objects.filter(patient_code=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Patient code already exists.")
        else:  # creating
            if Patient.objects.filter(patient_code=value).exists():
                raise serializers.ValidationError("Patient code already exists.")
        return value

    def validate_date_of_birth(self, value):
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        return value