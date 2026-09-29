from rest_framework import serializers

from .models import Biomarker


class BiomarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biomarker
        fields = [
            "id",
            "name",
            "code",
            "unit",
            "reference_min",
            "reference_max",
            "description",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class BiomarkerCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biomarker
        fields = ["name", "code", "unit", "reference_min", "reference_max", "description"]

    def validate_name(self, value):
        if self.instance:  # editing
            if Biomarker.objects.filter(name=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Biomarker name already exists.")
        else:  # creating
            if Biomarker.objects.filter(name=value).exists():
                raise serializers.ValidationError("Biomarker name already exists.")
        return value

    def validate_code(self, value):
        if self.instance:  # editing
            if Biomarker.objects.filter(code=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Biomarker code already exists.")
        else:  # creating
            if Biomarker.objects.filter(code=value).exists():
                raise serializers.ValidationError("Biomarker code already exists.")
        return value

    def validate(self, data):
        if data.get("reference_min") and data.get("reference_max"):
            if data["reference_min"] >= data["reference_max"]:
                raise serializers.ValidationError(
                    {"reference_min": "Min must be less than max."}
                )
        return data