from rest_framework import serializers

from .models import CartItem
from menu.models import MenuItem
from rest_framework import serializers
from .models import CartItem
from .models import Order, OrderItem


class OrderStatusSerializer(serializers.ModelSerializer):

    class Meta:

        model = Order

        fields = ['status']
        
class OrderItemSerializer(serializers.ModelSerializer):

    item_name = serializers.CharField(
        source='menu_item.name',
        read_only=True
    )

    class Meta:

        model = OrderItem

        fields = [
            'item_name',
            'quantity',
            'price'
        ]


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(
        source='order_items',
        many=True,
        read_only=True
    )

    class Meta:

        model = Order

        fields = [
            'id',
            'status',
            'total_price',
            'created_at',
            'items'
        ]

class CartItemSerializer(serializers.ModelSerializer):

    item_name = serializers.CharField(
        source='menu_item.name',
        read_only=True
    )

    item_price = serializers.DecimalField(
        source='menu_item.price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:

        model = CartItem

        fields = [
            'id',
            'item_name',
            'item_price',
            'quantity'
        ]

class AddToCartSerializer(serializers.Serializer):

    menu_item_id = serializers.IntegerField()

    quantity = serializers.IntegerField()

