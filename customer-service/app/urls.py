from django.urls import path

from .views import (
    CustomerViewSet,
    CustomerRegisterView,
    CustomerLoginView,
)

urlpatterns = [
    path("customers/", CustomerViewSet.as_view(), name="customer-list-create"),
    path("customers/<int:pk>/", CustomerViewSet.as_view(), name="customer-detail"),
    path("customers/register/", CustomerRegisterView.as_view(), name="customer-register"),
    path("customers/login/", CustomerLoginView.as_view(), name="customer-login"),
]