from rest_framework import serializers


class CheckoutSerializer(serializers.Serializer):

    coupon_code = serializers.CharField(
        required=False,
        allow_blank=True
    )