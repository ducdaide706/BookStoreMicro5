from django.urls import path

from . import views

urlpatterns = [
    path('staff/login/', views.staff_login, name='staff_login'),
    path('staff/customers/', views.staff_customer_list, name='staff_customer_list'),
    path('staff/add-book/', views.staff_add_book, name='staff_add_book'),
]

