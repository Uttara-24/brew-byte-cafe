from django.urls import path

from .views import (
    AddToCartView,
    OrderHistoryView,
    UpdateOrderStatusView,
    ViewCartView,
    PlaceOrderView
)

urlpatterns = [

    path(
        "cart/add/",
        AddToCartView.as_view()
    ),

    path(
        "cart/",
        ViewCartView.as_view()
    ),

    path(
        "place-order/",
        PlaceOrderView.as_view()
    ),

    path(
        "history/",
        OrderHistoryView.as_view()
    ),

    path(
        "status/<int:pk>/",
        UpdateOrderStatusView.as_view()
    ),
]