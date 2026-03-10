from django.urls import path
from .views import CommentListView, CommentCreateView

urlpatterns = [
    path('comments/<int:book_id>/', CommentListView.as_view(), name='comment-list'),
    path('comments/<int:book_id>/add/', CommentCreateView.as_view(), name='comment-add'),
]