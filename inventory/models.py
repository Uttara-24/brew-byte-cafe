from django.db import models

from menu.models import MenuItem


class Inventory(models.Model):

    menu_item = models.OneToOneField(

        MenuItem,

        on_delete=models.CASCADE,

        related_name='inventory'
    )

    quantity_available = models.PositiveIntegerField()

    low_stock_threshold = models.PositiveIntegerField(

        default=10
    )

    updated_at = models.DateTimeField(

        auto_now=True
    )

    def __str__(self):

        return self.menu_item.name
