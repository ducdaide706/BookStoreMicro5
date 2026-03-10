from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_customer, name='register_customer'),
    path('login/', views.login_customer, name='login_customer'),
    path('staff/login/', views.staff_login, name='staff_login'),
    path('staff/customers/', views.staff_customer_list, name='staff_customer_list'),
    path('staff/add-book/', views.staff_add_book, name='staff_add_book'),
    path('books/', views.book_list, name='book_list'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/<int:cart_id>/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('books/<int:book_id>/', views.book_detail, name='book_detail'),
    path('books/<int:book_id>/add_comment/', views.add_comment, name='comment-add'),
    path('cart/checkout/', views.checkout_cart, name='checkout_cart'),
    path('pay/', views.pay_order, name='pay_order'),
    path('pay/methods/', views.get_paymethod_list, name='get_paymethod_list'),
    path('orders/', views.order_list, name='order_list'),
]
