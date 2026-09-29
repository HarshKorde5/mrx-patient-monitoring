from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/patients/", include("apps.patients.urls")),
    path("api/v1/biomarkers/", include("apps.biomarkers.urls")),
    path("api/v1/results/", include("apps.results.urls")),
    path("api/v1/dashboard/", include("apps.dashboard.urls")),
    path("api/v1/reports/", include("apps.reports.urls")),
]