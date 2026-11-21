from decimal import Decimal

from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from orders.models import Cart
from coupons.models import Coupon

from .serializers import CheckoutSerializer


class CheckoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        # -----------------------------
        # STEP 1: Validate request
        # -----------------------------

        serializer = CheckoutSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        coupon_code = serializer.validated_data.get(
            "coupon_code"
        )

        # -----------------------------
        # STEP 2: Get user's cart
        # -----------------------------

        cart = Cart.objects.filter(
            customer=request.user
        ).first()

        if not cart:

            return Response({
                "message": "Cart is empty"
            }, status=400)

        cart_items = cart.cart_items.all()

        if not cart_items:

            return Response({
                "message": "Cart is empty"
            }, status=400)

        # -----------------------------
        # STEP 3: Calculate subtotal
        # -----------------------------

        subtotal = Decimal("0")

        items = []

        for item in cart_items:

            item_total = (
                item.menu_item.price *
                item.quantity
            )

            subtotal += item_total

            items.append({

                "menu_item_id":
                    item.menu_item.id,

                "name":
                    item.menu_item.name,

                "quantity":
                    item.quantity,

                "price":
                    item.menu_item.price,

                "item_total":
                    item_total
            })

        # -----------------------------
        # STEP 4: Apply coupon
        # -----------------------------

        discount = Decimal("0")
        applied_coupon = None

        if coupon_code:

            try:

                coupon = Coupon.objects.get(
                    code=coupon_code.upper()
                )

            except Coupon.DoesNotExist:

                return Response({
                    "message": "Invalid coupon code"
                }, status=400)

            # Check active
            if not coupon.is_active:

                return Response({
                    "message": "Coupon is inactive"
                }, status=400)

            # Check expiry
            if coupon.expiry_date < timezone.now():

                return Response({
                    "message": "Coupon has expired"
                }, status=400)

            # Check minimum order amount
            if subtotal < coupon.minimum_order_amount:

                return Response({

                    "message":
                    "Minimum order amount for this coupon is "
                    f"{coupon.minimum_order_amount}"

                }, status=400)

            # Calculate discount
            discount = (
                subtotal *
                coupon.discount_percentage /
                Decimal("100")
            )

            applied_coupon = coupon.code

        # -----------------------------
        # STEP 5: Calculate final amount
        # -----------------------------

        final_amount = subtotal - discount

        # -----------------------------
        # STEP 6: Return checkout
        # -----------------------------

        return Response({

            "items": items,

            "subtotal": subtotal,

            "discount": discount,

            "total": final_amount,

            "coupon": applied_coupon
        })