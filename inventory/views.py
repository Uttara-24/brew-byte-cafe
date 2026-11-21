from rest_framework import generics

from .models import Inventory

from .serializers import InventorySerializer


class InventoryListView(

    generics.ListAPIView
):

    queryset = Inventory.objects.all()

    serializer_class = InventorySerializer


class InventoryCreateView(

    generics.CreateAPIView
):

    queryset = Inventory.objects.all()

    serializer_class = InventorySerializer

class LowStockView(

    generics.ListAPIView
):

    serializer_class = InventorySerializer

    def get_queryset(self):

        return Inventory.objects.filter(

            quantity_available__lte=10
        )
