from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Ship
from .serializers import ShipSerializer

# Create your views here.

class ShipCreateView(APIView):
    def post(self, request):
        serializer = ShipSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ShipmentView(APIView):
    def post(self, request):
        order_id = request.data.get('order_id')
        address = request.data.get('address')
        if not order_id or not address:
            return Response({'error': 'Missing order_id or address'}, status=status.HTTP_400_BAD_REQUEST)
        shipment = Ship.objects.create(order_id=order_id, address=address)
        serializer = ShipSerializer(shipment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
