from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Coupon
from .serializers import CouponSerializer


class CreateCouponView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = CouponSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            serializer.data,
            status=201
        )

class ValidateCouponView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        code = request.data.get("code")

        if not code:

            return Response({
                "message": "Coupon code is required"
            }, status=400)

        try:

            coupon = Coupon.objects.get(
                code=code.upper()
            )

        except Coupon.DoesNotExist:

            return Response({
                "message": "Invalid coupon code"
            }, status=400)

        if not coupon.is_active:

            return Response({
                "message": "Coupon is inactive"
            }, status=400)

        if coupon.expiry_date < timezone.now():

            return Response({
                "message": "Coupon has expired"
            }, status=400)

        return Response({

            "message": "Coupon is valid",

            "coupon": CouponSerializer(
                coupon
            ).data
        })
