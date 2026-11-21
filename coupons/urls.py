from django.urls import path

from .views import (
    CreateCouponView,
    ValidateCouponView
)


urlpatterns = [

    path(
        "create/",
        CreateCouponView.as_view()
    ),

    path(
        "validate/",
        ValidateCouponView.as_view()
    ),
]