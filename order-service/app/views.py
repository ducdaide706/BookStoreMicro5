from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from .serializers import OrderSerializer

# Create your views here.

class CreateOrderFromCartView(APIView):
    def post(self, request):
        customer_id = request.data.get('customer_id')
        cart_items = request.data.get('cart_items', [])
        if not customer_id or not cart_items:
            return Response({'error': 'Missing customer_id or cart_items'}, status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.create(customer_id=customer_id)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book_id=item['book_id'],
                quantity=item['quantity'],
                price=item['price']
            )
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderListByCustomerView(APIView):
    def get(self, request):
        customer_id = request.GET.get('customer_id')
        if not customer_id:
            return Response({'error': 'Missing customer_id'}, status=status.HTTP_400_BAD_REQUEST)
        orders = Order.objects.filter(customer_id=customer_id).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
