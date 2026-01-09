from data.api.serializers import BieniciImportSerializer, ChargesStatsQuerySerializer
from data.models import Listing
from data.services.bienici import extract_bienici_id, fetch_bienici_ad, parse_bienici_ad
from data.services.stats import compute_charges_stats
from rest_framework import status
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


class ImportBieniciView(APIView):
    def post(self, request):
        ser = BieniciImportSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        url = ser.validated_data["url"]
        bienici_id = extract_bienici_id(url)

        payload = fetch_bienici_ad(bienici_id)
        ad = parse_bienici_ad(payload)

        listing, created = Listing.objects.update_or_create(
            source_id=ad.bienici_id,
            defaults={
                "city": ad.city,
                "postal_code": ad.postal_code,
                "department_code": ad.department_code,
                "annual_condominium_fees": ad.annual_fees,
            },
        )

        return Response(
            {
                "source_id": listing.source_id,
                "created": created,
                "city": listing.city,
                "postal_code": listing.postal_code,
                "department_code": listing.department_code,
                "annual_condominium_fees": (
                    str(listing.annual_condominium_fees)
                    if listing.annual_condominium_fees is not None
                    else None
                ),
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )
