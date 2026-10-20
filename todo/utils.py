from rest_framework.response import Response

def api_response(success=True, message="", data=None, status_code=200):
    return Response({
        "success": success,
        "status_code": status_code,
        "message": message,
        "data": data
    }, status=status_code)