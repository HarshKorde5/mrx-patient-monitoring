from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection


@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    """Health check endpoint. Returns 200 if DB is connected."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return Response({"status": "healthy", "database": "connected"})
    except Exception as e:
        return Response(
            {"status": "unhealthy", "database": "disconnected", "error": str(e)},
            status=503,
        )