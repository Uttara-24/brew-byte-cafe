from django.urls import path

from .views import (

    InventoryListView,

    InventoryCreateView,
    LowStockView
)

urlpatterns = [

    path(

        "list/",

        InventoryListView.as_view()
    ),

    path(

        "create/",

        InventoryCreateView.as_view()
    ),

    path(

        "low-stock/",

        LowStockView.as_view()
),
]