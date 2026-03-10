from django.db import models

class Ship(models.Model):
    order_id = models.IntegerField()
    address = models.CharField(max_length=255)
    shipped_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return f"Ship {self.id} - Order {self.order_id}"
