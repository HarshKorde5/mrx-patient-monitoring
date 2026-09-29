from django.db import transaction

from .models import Patient


@transaction.atomic
def create_patient(*, patient_code, full_name, date_of_birth, gender, medical_history, created_by):
    patient = Patient.objects.create(
        patient_code=patient_code,
        full_name=full_name,
        date_of_birth=date_of_birth,
        gender=gender,
        medical_history=medical_history,
        created_by=created_by,
    )
    return patient


@transaction.atomic
def update_patient(*, patient, patient_code, full_name, date_of_birth, gender, medical_history):
    patient.patient_code = patient_code
    patient.full_name = full_name
    patient.date_of_birth = date_of_birth
    patient.gender = gender
    patient.medical_history = medical_history
    patient.save()
    return patient


@transaction.atomic
def deactivate_patient(*, patient):
    """Soft delete: mark inactive instead of erasing."""
    patient.is_active = False
    patient.save()
    return patient