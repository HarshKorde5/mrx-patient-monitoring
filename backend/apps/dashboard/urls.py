from django.urls import path
from . import views

urlpatterns = [
    path("patient/<uuid:patient_id>/", views.patient_dashboard, name="patient_dashboard"),
    path("patient/<uuid:patient_id>/biomarkers/", views.patient_biomarkers, name="patient_biomarkers"),
]