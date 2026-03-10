from django.urls import path
from .views import CreateOrderFromCartView, OrderListByCustomerView

urlpatterns = [
    path('create/', CreateOrderFromCartView.as_view(), name='create_order'),
    path('orders/', OrderListByCustomerView.as_view(), name='order_list_by_customer'),
    # ...existing code...
]