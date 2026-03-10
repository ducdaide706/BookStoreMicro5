from django.db import models

class PayMethod(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Pay(models.Model):
    customer_id = models.IntegerField()
    order_id = models.IntegerField()
    pay_at = models.DateTimeField(auto_now_add=True)
    pay_method = models.ForeignKey(PayMethod, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Pay {self.id} - Order {self.order_id}"
