from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from .models import Reservation

from .serializers import ReservationSerializer


class CreateReservationView(APIView):

    permission_classes = [

        IsAuthenticated
    ]

    def post(self, request):

        serializer = ReservationSerializer(

            data=request.data
        )

        serializer.is_valid(

            raise_exception=True
        )

        table_exists = Reservation.objects.filter(

            table_number=serializer.validated_data[
                'table_number'
            ],

            reservation_date=serializer.validated_data[
                'reservation_date'
            ],

            reservation_time=serializer.validated_data[
                'reservation_time'
            ],

            status='booked'

        ).exists()

        if table_exists:

            return Response({

                "message":
                "Table already booked"

            }, status=400)

        serializer.save(

            customer=request.user
        )

        return Response(

            serializer.data,

            status=201
        )
    
class MyReservationsView(APIView):

    permission_classes = [

        IsAuthenticated
    ]

    def get(self, request):

        reservations = Reservation.objects.filter(

            customer=request.user

        ).order_by(

            '-reservation_date'
        )

        serializer = ReservationSerializer(

            reservations,

            many=True
        )

        return Response(

            serializer.data
        )
