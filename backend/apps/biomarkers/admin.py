from django.contrib import admin

from .models import Biomarker


@admin.register(Biomarker)
class BiomarkerAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "unit", "reference_min", "reference_max", "is_active")
    search_fields = ("name", "code")