from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .models import ExchangeRate
from .serializers import ExchangeRateSerializer


class ExchangeRateViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        rates = ExchangeRate.objects.all().order_by("currency_code")
        serializer = ExchangeRateSerializer(rates, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def exchange_rate_list(request):
    """API endpoint for live/cached exchange rates against USD."""
    rates = ExchangeRate.objects.all().order_by("currency_code")
    serializer = ExchangeRateSerializer(rates, many=True)
    return Response(serializer.data)