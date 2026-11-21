from django.urls import path

from .views import (

    CreateReservationView,

    MyReservationsView
)

urlpatterns = [

    path(

        "create/",

        CreateReservationView.as_view()
    ),

    path(

        "my/",

        MyReservationsView.as_view()
    ),
]