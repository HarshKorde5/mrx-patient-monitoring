from django.contrib import admin

from .models import TestResult


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ("patient", "biomarker", "value", "unit", "test_date", "recorded_by")
    list_filter = ("biomarker", "test_date")
    search_fields = ("patient__patient_code", "patient__full_name")