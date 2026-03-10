from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer

# Create your views here.

class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        book_id = self.kwargs.get('book_id')
        return Comment.objects.filter(book_id=book_id).order_by('-created_at')

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        book_id = self.kwargs.get('book_id')
        data = request.data.copy()
        data['book_id'] = book_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
