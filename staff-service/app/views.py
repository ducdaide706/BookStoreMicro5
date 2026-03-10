from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
import requests

CUSTOMER_SERVICE_URL = "http://localhost:8001"
BOOK_SERVICE_URL = "http://localhost:8003"

@csrf_protect
def staff_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'admin' and password == 'admin123':
            request.session['staff_logged_in'] = True
            messages.success(request, 'Đăng nhập thành công!')
            return redirect('staff_customer_list')
        else:
            messages.error(request, 'Sai tài khoản hoặc mật khẩu!')
    return render(request, 'staff_login.html')


def staff_customer_list(request):
    if not request.session.get('staff_logged_in'):
        return redirect('staff_login')
    customers = []
    try:
        resp = requests.get(f"{CUSTOMER_SERVICE_URL}/api/customers/", timeout=5)
        if resp.status_code == 200:
            customers = resp.json()
    except requests.RequestException:
        messages.error(request, 'Không thể kết nối Customer Service!')
    return render(request, 'staff_customer_list.html', {'customers': customers})


@csrf_protect
def staff_add_book(request):
    if not request.session.get('staff_logged_in'):
        return redirect('staff_login')
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        description = request.POST.get('description')
        stock = request.POST.get('stock')
        if not title or not author or not price or not stock:
            messages.error(request, 'Vui lòng nhập đủ thông tin!')
        else:
            try:
                resp = requests.post(
                    f"{BOOK_SERVICE_URL}/api/books/",
                    json={
                        'title': title,
                        'author': author,
                        'price': price,
                        'description': description,
                        'stock': stock
                    },
                    timeout=5
                )
                if resp.status_code == 201:
                    messages.success(request, 'Thêm sách thành công!')
                else:
                    messages.error(request, 'Không thể thêm sách!')
            except requests.RequestException:
                messages.error(request, 'Không thể kết nối Book Service!')
    return render(request, 'staff_add_book.html')
