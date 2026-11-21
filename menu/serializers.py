from rest_framework import serializers
from .models import Category, MenuItem


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):

    category_details = CategorySerializer(
        source='category',
        read_only=True
    )

    class Meta:
        model = MenuItem
        fields = [
            'id',
            'category',
            'category_details',
            'name',
            'description',
            'price',
            'is_available',
            'created_at'
        ]