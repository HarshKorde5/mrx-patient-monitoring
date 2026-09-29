from django.contrib import admin

from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("patient_code", "full_name", "gender", "date_of_birth", "is_active")
    search_fields = ("patient_code", "full_name")
    list_filter = ("gender", "is_active")