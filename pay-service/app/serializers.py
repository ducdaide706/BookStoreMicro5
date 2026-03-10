from rest_framework import serializers
from .models import Pay, PayMethod

class PayMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayMethod
        fields = ['id', 'name', 'description']

class PaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay
        fields = ['id', 'customer_id', 'order_id', 'pay_at', 'pay_method']