from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart, CartItem
from .serializers import (
    CartSerializer, 
    CartCreateSerializer, 
    CartItemSerializer,
    CartItemCreateSerializer
)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CartCreateSerializer
        return CartSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new cart for a customer"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = serializer.save()
        
        # Return the cart with items
        response_serializer = CartSerializer(cart)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'], url_path='customer/(?P<customer_id>[^/.]+)')
    def get_by_customer(self, request, customer_id=None):
        """Get cart by customer ID"""
        try:
            cart = Cart.objects.get(customer_id=customer_id)
            serializer = self.get_serializer(cart)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response(
                {'detail': 'Cart not found for this customer'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'], url_path='add-item')
    def add_item(self, request, pk=None):
        """Add item to cart"""
        cart = self.get_object()
        serializer = CartItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Check if item already exists in cart
        book_id = serializer.validated_data['book_id']
        quantity = serializer.validated_data['quantity']
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            book_id=book_id,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Update quantity if item already exists
            cart_item.quantity += quantity
            cart_item.save()
        
        # Return updated cart
        response_serializer = CartSerializer(cart)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'], url_path='remove-item/(?P<item_id>[^/.]+)')
    def remove_item(self, request, pk=None, item_id=None):
        """Remove item from cart"""
        cart = self.get_object()
        try:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            cart_item.delete()
            
            # Return updated cart
            response_serializer = CartSerializer(cart)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response(
                {'detail': 'Item not found in cart'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['put'], url_path='update-item/(?P<item_id>[^/.]+)')
    def update_item(self, request, pk=None, item_id=None):
        """Update item quantity in cart"""
        cart = self.get_object()
        try:
            cart_item = CartItem.objects.get(id=item_id, cart=cart)
            
            quantity = request.data.get('quantity')
            if quantity is not None:
                cart_item.quantity = quantity
                cart_item.save()
            
            # Return updated cart
            response_serializer = CartSerializer(cart)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except CartItem.DoesNotExist:
            return Response(
                {'detail': 'Item not found in cart'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['delete'], url_path='clear')
    def clear_cart(self, request, pk=None):
        """Clear all items from cart"""
        cart = self.get_object()
        CartItem.objects.filter(cart=cart).delete()
        
        # Return empty cart
        response_serializer = CartSerializer(cart)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
