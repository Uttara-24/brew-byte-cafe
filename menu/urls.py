from django.urls import path

from .views import (
    CategoryListView,
    MenuItemListView,
    MenuItemCreateView,
    MenuItemUpdateView,
    MenuItemDeleteView,
)

urlpatterns = [

    path(
        'categories/',
        CategoryListView.as_view()
    ),

    path(
        'items/',
        MenuItemListView.as_view()
    ),

    path(
        'items/create/',
        MenuItemCreateView.as_view()
    ),

    path(
        'items/update/<int:pk>/',
        MenuItemUpdateView.as_view()
    ),

    path(
        'items/delete/<int:pk>/',
        MenuItemDeleteView.as_view()
    ),
]