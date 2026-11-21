
from rest_framework import serializers

from .models import Inventory


class InventorySerializer(

    serializers.ModelSerializer
):

    item_name = serializers.CharField(

        source='menu_item.name',

        read_only=True
    )

    class Meta:

        model = Inventory

        fields = '__all__'