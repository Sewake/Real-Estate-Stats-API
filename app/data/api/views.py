from data.api.serializers import ChargesStatsQuerySerializer
from data.services.stats import compute_charges_stats
from rest_framework.response import Response
from rest_framework.views import APIView


class ChargesStatsView(APIView):
    def get(self, request):
        ser = ChargesStatsQuerySerializer(data=request.query_params)
        ser.is_valid(raise_exception=True)

        stats = compute_charges_stats(**ser.validated_data)

        return Response(
            {
                "count": stats.count,
                "mean": str(stats.mean),
                "q10": str(stats.q10),
                "q90": str(stats.q90),
            }
        )
