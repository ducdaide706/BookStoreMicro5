from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        """Update book stock"""
        book = self.get_object()
        quantity = request.data.get('quantity')
        
        if quantity is None:
            return Response(
                {'detail': 'Quantity is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            quantity = int(quantity)
        except ValueError:
            return Response(
                {'detail': 'Quantity must be a number'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        book.stock += quantity
        if book.stock < 0:
            return Response(
                {'detail': 'Insufficient stock'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get books with stock > 0"""
        books = Book.objects.filter(stock__gt=0)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
