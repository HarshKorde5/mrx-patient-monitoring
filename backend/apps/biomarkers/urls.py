from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("", views.BiomarkerViewSet, basename="biomarker")

urlpatterns = router.urls