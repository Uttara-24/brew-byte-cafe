from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Category, MenuItem

from .serializers import (
    CategorySerializer,
    MenuItemSerializer
)

from .permissions import IsAdminOrStaff


# VIEW ALL CATEGORIES
class CategoryListView(generics.ListAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


# VIEW ALL MENU ITEMS
class MenuItemListView(generics.ListAPIView):

    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [AllowAny]


# ADD MENU ITEM
class MenuItemCreateView(generics.CreateAPIView):

    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrStaff]


# UPDATE MENU ITEM
class MenuItemUpdateView(generics.UpdateAPIView):

    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrStaff]


# DELETE MENU ITEM
class MenuItemDeleteView(generics.DestroyAPIView):

    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminOrStaff]