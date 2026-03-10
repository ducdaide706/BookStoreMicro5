from .views import PayMethodListView, PayView
from django.urls import path

urlpatterns = [
    path('pay/methods/', PayMethodListView.as_view(), name='pay_method_list'),
    path('pay/', PayView.as_view(), name='pay'),
    # ...existing code...
]