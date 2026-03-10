from django.shortcuts import render
from rest_framework import generics
from .models import Catalog, CatalogBook
from .serializers import CatalogSerializer, CatalogBookSerializer

# Create your views here.

class CatalogListView(generics.ListAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer

class CatalogBookListView(generics.ListAPIView):
    queryset = CatalogBook.objects.all()
    serializer_class = CatalogBookSerializer
