from rest_framework import serializers
from .models import Catalog, CatalogBook

class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ['id', 'name', 'description']

class CatalogBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogBook
        fields = ['id', 'catalog', 'book_id']