from decimal import Decimal

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from inventory.models import Inventory
from menu.models import MenuItem

from .models import Cart, CartItem, Order, OrderItem

from .permissions import IsAdminOrStaff

from .serializers import (
    AddToCartSerializer,
    CartItemSerializer,
    OrderSerializer,
    OrderStatusSerializer
)

class UpdateOrderStatusView(APIView):

    permission_classes = [IsAdminOrStaff]

    def patch(self, request, pk):

        try:

            order = Order.objects.get(

                id=pk
            )

        except Order.DoesNotExist:

            return Response({

                "message": "Order not found"

            }, status=404)

        serializer = OrderStatusSerializer(

            order,

            data=request.data,

            partial=True
        )

        serializer.is_valid(

            raise_exception=True
        )

        serializer.save()

        return Response({

            "message": "Status updated",

            "status": serializer.data
        })

class ViewCartView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        cart = Cart.objects.filter(
            customer=request.user
        ).first()

        if not cart:

            return Response({
                "message": "Cart empty"
            })

        cart_items = cart.cart_items.all()

        serializer = CartItemSerializer(
            cart_items,
            many=True
        )

        total = Decimal("0")

        for item in cart_items:

            total += (
                item.menu_item.price *
                item.quantity
            )

        return Response({

            "items": serializer.data,

            "total_price": total
        })

class AddToCartView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = AddToCartSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        cart, created = Cart.objects.get_or_create(
            customer=request.user
        )

        menu_item = MenuItem.objects.get(
            id=serializer.validated_data[
                "menu_item_id"
            ]
        )

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            menu_item=menu_item
        )

        cart_item.quantity += serializer.validated_data[
            "quantity"
        ]

        cart_item.save()

        return Response({
            "message": "Added to cart"
        })

class PlaceOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        cart = Cart.objects.filter(
            customer=request.user
        ).first()

        if not cart:
            return Response({
                "message": "Cart empty"
            }, status=400)

        cart_items = cart.cart_items.all()

        if not cart_items:
            return Response({
                "message": "Cart empty"
            }, status=400)

        # STEP 1: Check inventory for all items
        for item in cart_items:

            try:
                inventory = Inventory.objects.get(
                    menu_item=item.menu_item
                )

            except Inventory.DoesNotExist:
                return Response({
                    "message":
                    f"Inventory not available for "
                    f"{item.menu_item.name}"
                }, status=400)

            if inventory.quantity_available < item.quantity:
                return Response({
                    "message":
                    f"Not enough stock for "
                    f"{item.menu_item.name}"
                }, status=400)

        # STEP 2: Create order
        order = Order.objects.create(
            customer=request.user
        )

        total = Decimal("0")

        # STEP 3: Create order items + reduce inventory
        for item in cart_items:

            inventory = Inventory.objects.get(
                menu_item=item.menu_item
            )

            OrderItem.objects.create(
                order=order,
                menu_item=item.menu_item,
                quantity=item.quantity,
                price=item.menu_item.price
            )

            inventory.quantity_available -= item.quantity
            inventory.save()

            total += (
                item.menu_item.price *
                item.quantity
            )

        # STEP 4: Save total
        order.total_price = total
        order.save()

        # STEP 5: Clear cart
        cart_items.delete()

        return Response({

            "message": "Order placed",

            "order_id": order.id,

            "total": total
        })

class OrderHistoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        orders = Order.objects.filter(
            customer=request.user
        ).order_by('-created_at')

        serializer = OrderSerializer(
            orders,
            many=True
        )

        return Response(
            serializer.data
        )