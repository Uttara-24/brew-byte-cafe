import uuid
from decimal import Decimal

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from orders.models import Cart, Order, OrderItem
from inventory.models import Inventory

from .models import Payment
from .serializers import PaymentSerializer


class CreatePaymentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        # -----------------------------
        # STEP 1: Get user's cart
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
        # STEP 2: Calculate subtotal
        # -----------------------------

        subtotal = Decimal("0")

        for item in cart_items:

            subtotal += (
                item.menu_item.price *
                item.quantity
            )

        # -----------------------------
        # STEP 3: Get coupon
        # -----------------------------

        coupon_code = request.data.get(
            "coupon_code"
        )

        discount = Decimal("0")

        if coupon_code:

            from coupons.models import Coupon
            from django.utils import timezone

            try:

                coupon = Coupon.objects.get(
                    code=coupon_code.upper()
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

            if subtotal < coupon.minimum_order_amount:

                return Response({
                    "message":
                    "Minimum order amount for this coupon is "
                    f"{coupon.minimum_order_amount}"
                }, status=400)

            discount = (
                subtotal *
                coupon.discount_percentage /
                Decimal("100")
            )

        # -----------------------------
        # STEP 4: Calculate final amount
        # -----------------------------

        final_amount = subtotal - discount

        # -----------------------------
        # STEP 5: Validate payment method
        # -----------------------------

        payment_method = request.data.get(
            "payment_method"
        )

        allowed_methods = [
            "card",
            "upi",
            "cash"
        ]

        if payment_method not in allowed_methods:

            return Response({
                "message":
                "Invalid payment method"
            }, status=400)

        # -----------------------------
        # STEP 6: Simulate payment
        # -----------------------------

        payment_success = True

        if not payment_success:

            return Response({
                "message": "Payment failed"
            }, status=400)

        # -----------------------------
        # STEP 7: Create Payment
        # -----------------------------

        transaction_id = (
            "TXN-" +
            uuid.uuid4().hex[:12].upper()
        )

        payment = Payment.objects.create(

            customer=request.user,

            amount=final_amount,

            payment_method=payment_method,

            status="success",

            transaction_id=transaction_id
        )

        # -----------------------------
        # STEP 8: Create Order
        # -----------------------------

        order = Order.objects.create(

            customer=request.user,

            total_price=final_amount,

            status="pending"
        )

        # -----------------------------
        # STEP 9: Create Order Items
        # -----------------------------

        for item in cart_items:

            inventory = Inventory.objects.get(

                menu_item=item.menu_item
            )

            if inventory.quantity_available < item.quantity:

                payment.status = "failed"

                payment.save()

                order.delete()

                return Response({

                    "message":
                    f"Not enough stock for "
                    f"{item.menu_item.name}"

                }, status=400)

            OrderItem.objects.create(

                order=order,

                menu_item=item.menu_item,

                quantity=item.quantity,

                price=item.menu_item.price
            )

            inventory.quantity_available -= (
                item.quantity
            )

            inventory.save()

        # -----------------------------
        # STEP 10: Clear Cart
        # -----------------------------

        cart_items.delete()

        # -----------------------------
        # STEP 11: Return Response
        # -----------------------------

        return Response({

            "message":
            "Payment successful",

            "payment": PaymentSerializer(
                payment
            ).data,

            "order_id":
            order.id,

            "total":
            final_amount
        }, status=201)
