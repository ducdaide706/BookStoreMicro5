from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Pay, PayMethod
from .serializers import PaySerializer, PayMethodSerializer

# Create your views here.

class PayMethodListView(APIView):
    def get(self, request):
        methods = PayMethod.objects.all()
        serializer = PayMethodSerializer(methods, many=True)
        return Response(serializer.data)

class PayView(APIView):
    def post(self, request):
        serializer = PaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
