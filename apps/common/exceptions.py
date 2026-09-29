from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None

    data = response.data
    if isinstance(data, dict) and "detail" in data:
        message, details = str(data["detail"]), None
    else:
        message, details = "Invalid input", data

    code_map = {
        400: "validation_error",
        401: "not_authenticated",
        403: "permission_denied",
        404: "not_found",
        429: "throttled",
    }
    response.data = {
        "error": {
            "code": code_map.get(response.status_code, "error"),
            "message": message,
            "details": details,
        }
    }
    return response