from django.urls import path
from . import views

urlpatterns = [
    path("patient/<uuid:patient_id>/", views.report_data, name="report_data"),
    path("patient/<uuid:patient_id>/pdf/", views.report_pdf, name="report_pdf"),
]