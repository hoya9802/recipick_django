"""
Core vies for app.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def update_check(request):
    """Returns successful response."""
    return Response({'update': True})
