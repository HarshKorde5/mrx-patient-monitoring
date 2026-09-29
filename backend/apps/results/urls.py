from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("", views.TestResultViewSet, basename="result")

urlpatterns = router.urls