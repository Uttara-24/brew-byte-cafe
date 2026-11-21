from django.db import models
from users.models import User


class Reservation(models.Model):

    STATUS_CHOICES = (

        ('booked', 'Booked'),

        ('completed', 'Completed'),

        ('cancelled', 'Cancelled')
    )

    customer = models.ForeignKey(

        User,

        on_delete=models.CASCADE,

        related_name='reservations'
    )

    table_number = models.IntegerField()

    reservation_date = models.DateField()

    reservation_time = models.TimeField()

    number_of_people = models.PositiveIntegerField()

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default='booked'
    )

    created_at = models.DateTimeField(

        auto_now_add=True
    )

    def __str__(self):

        return f"{self.customer.username} - Table {self.table_number}"
