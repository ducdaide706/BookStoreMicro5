from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'book_id', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True, source='cartitem_set')
    
    class Meta:
        model = Cart
        fields = ['id', 'customer_id', 'items']
        read_only_fields = ['id']


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['book_id', 'quantity']


class CartCreateSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    items = CartItemCreateSerializer(many=True, required=False)
    
    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        cart = Cart.objects.create(**validated_data)
        
        for item_data in items_data:
            CartItem.objects.create(cart=cart, **item_data)
        
        return cart
