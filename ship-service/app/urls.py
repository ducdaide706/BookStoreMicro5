from .views import ShipCreateView, ShipmentView
from django.urls import path

urlpatterns = [
    path('ship/', ShipCreateView.as_view(), name='ship_create'),
    path('shipment/', ShipmentView.as_view(), name='shipment_post'),
    # ...existing code...
]
