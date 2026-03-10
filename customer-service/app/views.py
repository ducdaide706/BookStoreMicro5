import os

import requests
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Customer
from .serializers import CustomerSerializer, CustomerRegisterSerializer

CART_SERVICE_URL = os.getenv("CART_SERVICE_URL", "http://localhost:8002")


class CustomerViewSet(APIView):
	"""
	API chỉ để xem danh sách / chi tiết customer (GET).
	Đăng ký và đăng nhập dùng các endpoint riêng: CustomerRegisterView, CustomerLoginView.
	"""

	def get_object(self, pk):
		try:
			return Customer.objects.get(pk=pk)
		except Customer.DoesNotExist:
			return None

	def get(self, request, pk=None):
		if pk is None:
			customers = Customer.objects.all().order_by("id")
			serializer = CustomerSerializer(customers, many=True)
			return Response(serializer.data)

		customer = self.get_object(pk)
		if customer is None:
			return Response({"detail": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

		serializer = CustomerSerializer(customer)
		return Response(serializer.data)


class CustomerRegisterView(APIView):
	"""
	Đăng ký tài khoản customer với mật khẩu.
	POST /api/customers/register/
	body: { "name": "...", "email": "...", "password": "..." }
	"""

	def post(self, request):
		serializer = CustomerRegisterSerializer(data=request.data)
		if serializer.is_valid():
			customer = serializer.save()
			# Tạo cart tương ứng như luồng cũ
			try:
				requests.post(
					f"{CART_SERVICE_URL}/api/carts/",
					json={"customer_id": customer.id},
					timeout=5,
				)
			except requests.RequestException:
				# Không fail nghiệp vụ đăng ký nếu cart-service lỗi
				pass

			return Response(
				CustomerSerializer(customer).data,
				status=status.HTTP_201_CREATED,
			)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerLoginView(APIView):
	"""
	Đăng nhập customer.
	POST /api/customers/login/
	body: { "email": "...", "password": "..." }
	"""

	def post(self, request):
		email = request.data.get("email")
		password = request.data.get("password")

		if not email or not password:
			return Response(
				{"detail": "Email và password là bắt buộc."},
				status=status.HTTP_400_BAD_REQUEST,
			)

		try:
			customer = Customer.objects.get(email=email)
		except Customer.DoesNotExist:
			return Response(
				{"detail": "Thông tin đăng nhập không chính xác."},
				status=status.HTTP_400_BAD_REQUEST,
			)

		if not customer.password or not check_password(password, customer.password):
			return Response(
				{"detail": "Thông tin đăng nhập không chính xác."},
				status=status.HTTP_400_BAD_REQUEST,
			)

		return Response(CustomerSerializer(customer).data, status=status.HTTP_200_OK)
