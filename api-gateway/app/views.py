import os
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

CUSTOMER_SERVICE_URL = os.getenv("CUSTOMER_SERVICE_URL", "http://localhost:8001")
BOOK_SERVICE_URL = os.getenv("BOOK_SERVICE_URL", "http://localhost:8003")
CART_SERVICE_URL = os.getenv("CART_SERVICE_URL", "http://localhost:8002")
COMMENT_SERVICE_URL = os.getenv("COMMENT_SERVICE_URL", "http://localhost:8004")


def home(request):
    """Homepage with links to all features"""
    return render(request, 'home.html')



def register_customer(request):
    """Display customer registration form and handle submission"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not name or not email or not password:
            messages.error(request, 'Vui lòng điền đầy đủ họ tên, email và mật khẩu!')
            return render(request, 'register.html')
        
        try:
            # Call customer service API to register customer (có mật khẩu)
            response = requests.post(
                f"{CUSTOMER_SERVICE_URL}/api/customers/register/",
                json={"name": name, "email": email, "password": password},
                timeout=5
            )
            
            if response.status_code == 201:
                customer_data = response.json()
                messages.success(request, f'Đăng ký thành công! Chào mừng {customer_data["name"]}!')
                return redirect('customer_list')
            else:
                error_msg = response.json().get('email', ['Email đã tồn tại hoặc không hợp lệ'])[0]
                messages.error(request, f'Lỗi: {error_msg}')
        except requests.RequestException as e:
            messages.error(request, f'Không thể kết nối đến Customer Service. Vui lòng thử lại!')
        
        return render(request, 'register.html')

    return render(request, 'register.html')



def login_customer(request):
    """Display customer login form and handle submission"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Vui lòng nhập đầy đủ email và mật khẩu!')
            return render(request, 'login.html')

        try:
            response = requests.post(
                f"{CUSTOMER_SERVICE_URL}/api/customers/login/",
                json={"email": email, "password": password},
                timeout=5,
            )

            if response.status_code == 200:
                customer_data = response.json()
                # Lưu customer_id vào session để dùng cho mua sắm
                request.session['customer_id'] = customer_data['id']
                messages.success(request, f'Đăng nhập thành công! Chào mừng {customer_data["name"]}!')
                return redirect('book_list')
            else:
                error_msg = response.json().get('detail', 'Thông tin đăng nhập không chính xác!')
                messages.error(request, error_msg)
        except requests.RequestException:
            messages.error(request, 'Không thể kết nối đến Customer Service. Vui lòng thử lại!')

        return render(request, 'login.html')

    return render(request, 'login.html')


def customer_list(request):
    """Display list of all customers"""
    try:
        response = requests.get(
            f"{CUSTOMER_SERVICE_URL}/api/customers/",
            timeout=5
        )
        
        if response.status_code == 200:
            customers = response.json()
        else:
            customers = []
            messages.error(request, 'Không thể tải danh sách khách hàng')
    except requests.RequestException:
        customers = []
        messages.error(request, 'Không thể kết nối đến Customer Service')
    
    return render(request, 'customer_list.html', {'customers': customers})


def book_list(request):
    """Display list of all books"""
    # Lấy danh sách sách
    try:
        books_response = requests.get(f"{BOOK_SERVICE_URL}/api/books/", timeout=5)
        books = books_response.json() if books_response.status_code == 200 else []
    except requests.RequestException:
        books = []
        messages.error(request, 'Không thể kết nối Book Service')

    # Lấy danh sách catalog
    try:
        catalogs_response = requests.get("http://localhost:8005/api/catalogs/", timeout=5)
        catalogs = catalogs_response.json() if catalogs_response.status_code == 200 else []
    except requests.RequestException:
        catalogs = []
        messages.error(request, 'Không thể kết nối Catalog Service')

    # Lấy mapping CatalogBook
    try:
        mapping_response = requests.get("http://localhost:8005/api/catalog_books/", timeout=5)
        catalog_books = mapping_response.json() if mapping_response.status_code == 200 else []
    except requests.RequestException:
        catalog_books = []
        messages.error(request, 'Không thể kết nối Catalog Service')

    # Xây dựng cấu trúc catalogs_with_books
    book_dict = {book['id']: book for book in books}
    catalogs_with_books = []
    for cat in catalogs:
        book_ids = [m['book_id'] for m in catalog_books if m['catalog'] == cat['id']]
        cat_books = [book_dict[b_id] for b_id in book_ids if b_id in book_dict]
        catalogs_with_books.append({
            'catalog': cat,
            'books': cat_books
        })

    customer_id = request.session.get('customer_id') or request.GET.get('customer_id')
    return render(request, 'book_list.html', {
        'catalogs_with_books': catalogs_with_books,
        'customer_id': customer_id
    })


def add_to_cart(request):
    """Add book to cart"""
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        book_id = request.POST.get('book_id')
        quantity = request.POST.get('quantity', 1)
        
        if not customer_id:
            messages.error(request, 'Vui lòng chọn khách hàng trước!')
            return redirect('book_list')
        
        try:
            # Get or create cart for customer
            cart_response = requests.get(
                f"{CART_SERVICE_URL}/api/carts/customer/{customer_id}/",
                timeout=5
            )
            
            if cart_response.status_code == 404:
                # Create new cart
                create_cart_response = requests.post(
                    f"{CART_SERVICE_URL}/api/carts/",
                    json={"customer_id": int(customer_id)},
                    timeout=5
                )
                if create_cart_response.status_code == 201:
                    cart_data = create_cart_response.json()
                    cart_id = cart_data['id']
                else:
                    messages.error(request, 'Không thể tạo giỏ hàng!')
                    return redirect('book_list')
            elif cart_response.status_code == 200:
                cart_data = cart_response.json()
                cart_id = cart_data['id']
            else:
                messages.error(request, 'Không thể lấy thông tin giỏ hàng!')
                return redirect('book_list')
            
            # Add item to cart
            add_response = requests.post(
                f"{CART_SERVICE_URL}/api/carts/{cart_id}/add-item/",
                json={"book_id": int(book_id), "quantity": int(quantity)},
                timeout=5
            )
            
            if add_response.status_code == 200:
                messages.success(request, 'Đã thêm sách vào giỏ hàng!')
                # Store customer_id in session
                request.session['customer_id'] = customer_id
                return redirect('view_cart')
            else:
                messages.error(request, 'Không thể thêm sách vào giỏ hàng!')
        except requests.RequestException:
            messages.error(request, 'Không thể kết nối đến Cart Service!')
        
        return redirect('book_list')
    
    return redirect('book_list')


def view_cart(request):
    """View cart contents"""
    customer_id = request.session.get('customer_id') or request.GET.get('customer_id')
    
    if not customer_id:
        messages.error(request, 'Vui lòng chọn khách hàng!')
        return redirect('customer_list')
    
    cart_items = []
    total_price = 0
    customer = None
    cart_id = None
    
    try:
        # Get customer info
        customer_response = requests.get(
            f"{CUSTOMER_SERVICE_URL}/api/customers/{customer_id}/",
            timeout=5
        )
        if customer_response.status_code == 200:
            customer = customer_response.json()
        
        # Get cart
        cart_response = requests.get(
            f"{CART_SERVICE_URL}/api/carts/customer/{customer_id}/",
            timeout=5
        )
        
        if cart_response.status_code == 200:
            cart_data = cart_response.json()
            cart_id = cart_data['id']
            
            # Get book details for each cart item
            for item in cart_data.get('items', []):
                book_response = requests.get(
                    f"{BOOK_SERVICE_URL}/api/books/{item['book_id']}/",
                    timeout=5
                )
                if book_response.status_code == 200:
                    book = book_response.json()
                    item_total = float(book['price']) * item['quantity']
                    cart_items.append({
                        'id': item['id'],
                        'book': book,
                        'quantity': item['quantity'],
                        'total': item_total
                    })
                    total_price += item_total
        elif cart_response.status_code == 404:
            messages.info(request, 'Giỏ hàng trống!')
    except requests.RequestException:
        messages.error(request, 'Không thể tải giỏ hàng!')
    
    request.session['customer_id'] = customer_id
    
    return render(request, 'cart.html', {
        'customer': customer,
        'customer_id': customer_id,
        'cart_id': cart_id,
        'cart_items': cart_items,
        'total_price': total_price
    })


def remove_from_cart(request, cart_id, item_id):
    """Remove item from cart"""
    if request.method == 'POST':
        try:
            response = requests.delete(
                f"{CART_SERVICE_URL}/api/carts/{cart_id}/remove-item/{item_id}/",
                timeout=5
            )
            
            if response.status_code == 200:
                messages.success(request, 'Đã xóa sách khỏi giỏ hàng!')
            else:
                messages.error(request, 'Không thể xóa sách khỏi giỏ hàng!')
        except requests.RequestException:
            messages.error(request, 'Không thể kết nối đến Cart Service!')
    
    return redirect('view_cart')


def select_customer(request):
    """Select customer to shop"""
    try:
        response = requests.get(
            f"{CUSTOMER_SERVICE_URL}/api/customers/",
            timeout=5
        )
        
        if response.status_code == 200:
            customers = response.json()
        else:
            customers = []
            messages.error(request, 'Không thể tải danh sách khách hàng')
    except requests.RequestException:
        customers = []
        messages.error(request, 'Không thể kết nối đến Customer Service')
    
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        if customer_id:
            request.session['customer_id'] = customer_id
            return redirect('book_list')
    
    return render(request, 'select_customer.html', {'customers': customers})


def staff_customer_list(request):
    """
    Trang dành cho nhân viên xem danh sách khách hàng.
    Gọi trực tiếp Customer Service qua API.
    """
    customers = []
    error = None

    try:
        response = requests.get(f"{CUSTOMER_SERVICE_URL}/api/customers/", timeout=5)
        if response.status_code == 200:
            customers = response.json()
        else:
            error = 'Không thể tải danh sách khách hàng từ Customer Service.'
    except requests.RequestException:
        error = 'Không thể kết nối đến Customer Service.'

    if error:
        messages.error(request, error)

    return render(request, 'staff_customer_list.html', {'customers': customers})


def book_detail(request, book_id):
    # Lấy thông tin sách
    book = None
    try:
        resp = requests.get(f"{BOOK_SERVICE_URL}/api/books/{book_id}/", timeout=5)
        if resp.status_code == 200:
            book = resp.json()
        else:
            messages.error(request, "Không thể tải thông tin sách.")
    except requests.RequestException:
        messages.error(request, "Không thể kết nối Book Service.")

    # Lấy danh sách đánh giá
    comments = []
    try:
        resp = requests.get(f"{COMMENT_SERVICE_URL}/api/comments/{book_id}/", timeout=5)
        if resp.status_code == 200:
            comments = resp.json()
    except requests.RequestException:
        messages.error(request, "Không thể kết nối Comment Service.")

    return render(request, "book_detail.html", {"book": book, "comments": comments})


def add_comment(request, book_id):
    if request.method == "POST":
        content = request.POST.get("content")
        star = request.POST.get("star")
        if not content or not star:
            messages.error(request, "Vui lòng nhập nội dung và chọn số sao!")
            return redirect("book_detail", book_id=book_id)
        try:
            resp = requests.post(
                f"{COMMENT_SERVICE_URL}/api/comments/{book_id}/add/",
                json={"content": content, "star": int(star)},
                timeout=5
            )
            if resp.status_code == 201:
                messages.success(request, "Đánh giá thành công!")
            else:
                messages.error(request, "Không thể gửi đánh giá.")
        except requests.RequestException:
            messages.error(request, "Không thể kết nối Comment Service.")
        return redirect("book_detail", book_id=book_id)

CUSTOMER_SERVICE_URL = "http://localhost:8001"
BOOK_SERVICE_URL = "http://localhost:8003"


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


def checkout_cart(request):
    """Thanh toán giỏ hàng, tạo order từ cart"""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.error(request, 'Vui lòng đăng nhập để thanh toán!')
        return redirect('view_cart')
    cart_items = []
    total_price = 0
    cart_id = None
    try:
        cart_response = requests.get(
            f"{CART_SERVICE_URL}/api/carts/customer/{customer_id}/",
            timeout=5
        )
        if cart_response.status_code == 200:
            cart_data = cart_response.json()
            cart_id = cart_data['id']
            for item in cart_data.get('items', []):
                book_response = requests.get(
                    f"{BOOK_SERVICE_URL}/api/books/{item['book_id']}/",
                    timeout=5
                )
                if book_response.status_code == 200:
                    book = book_response.json()
                    cart_items.append({
                        'book_id': item['book_id'],
                        'quantity': item['quantity'],
                        'price': book['price']
                    })
        else:
            messages.error(request, 'Giỏ hàng trống hoặc không tồn tại!')
            return redirect('view_cart')
    except requests.RequestException:
        messages.error(request, 'Không thể kết nối đến Cart Service!')
        return redirect('view_cart')
    # Gọi order-service để tạo order
    try:
        order_response = requests.post(
            f"http://localhost:8007/app/create/",
            json={
                'customer_id': customer_id,
                'cart_items': cart_items
            },
            timeout=5
        )
        if order_response.status_code == 201:
            messages.success(request, 'Đặt hàng thành công!')
            # Xóa giỏ hàng nếu cần
            return redirect('book_list')
        else:
            messages.error(request, 'Đặt hàng thất bại!')
            return redirect('view_cart')
    except requests.RequestException:
        messages.error(request, 'Không thể kết nối đến Order Service!')
        return redirect('view_cart')


@csrf_protect
def pay_order(request):
    """Giao diện chọn phương pháp trả và trả tiền cho order"""
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        pay_method_id = request.POST.get('pay_method_id')
        customer_id = request.session.get('customer_id')
        address = request.POST.get('address')
        if not order_id or not pay_method_id or not customer_id or not address:
            messages.error(request, 'Thiếu thông tin thanh toán!')
            return redirect('view_cart')
        # Gọi pay-service để tạo pay
        try:
            response = requests.post(
                'http://localhost:8008/pay/',
                json={
                    'customer_id': customer_id,
                    'order_id': order_id,
                    'pay_method': pay_method_id
                },
                timeout=5
            )
            if response.status_code == 201:
                # Gọi ship-service để tạo shipment
                try:
                    ship_response = requests.post(
                        'http://localhost:8009/shipment/',
                        json={
                            'order_id': order_id,
                            'address': address
                        },
                        timeout=5
                    )
                    if ship_response.status_code == 201:
                        messages.success(request, 'Thanh toán và tạo shipment thành công!')
                        return redirect('book_list')
                    else:
                        messages.warning(request, 'Thanh toán thành công nhưng tạo shipment thất bại!')
                        return redirect('book_list')
                except requests.RequestException:
                    messages.warning(request, 'Thanh toán thành công nhưng không thể kết nối Ship Service!')
                    return redirect('book_list')
            else:
                messages.error(request, 'Thanh toán thất bại!')
                return redirect('view_cart')
        except requests.RequestException:
            messages.error(request, 'Không thể kết nối đến Pay Service!')
            return redirect('view_cart')
    else:
        # GET: lấy order_id từ query, lấy danh sách phương pháp trả
        order_id = request.GET.get('order_id')
        customer_id = request.session.get('customer_id')
        if not order_id or not customer_id:
            messages.error(request, 'Thiếu thông tin đơn hàng!')
            return redirect('view_cart')
        try:
            methods_response = requests.get('http://localhost:8008/methods/', timeout=5)
            if methods_response.status_code == 200:
                pay_methods = methods_response.json()
            else:
                pay_methods = []
        except requests.RequestException:
            pay_methods = []
        return render(request, 'pay.html', {
            'order_id': order_id,
            'pay_methods': pay_methods
        })



def order_list(request):
    """Danh sách đơn hàng đã đặt của khách hàng"""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        messages.error(request, 'Vui lòng đăng nhập để xem đơn hàng!')
        return redirect('login.html')
    try:
        response = requests.get(f'http://localhost:8007/app/orders/?customer_id={customer_id}', timeout=5)
        if response.status_code == 200:
            orders = response.json()
        else:
            orders = []
    except requests.RequestException:
        orders = []
    return render(request, 'order_list.html', {'orders': orders})


def get_paymethod_list():
    """API lấy danh sách phương pháp trả từ pay-service"""
    try:
        response = requests.get('http://localhost:8008/methods/', timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return []
    except requests.RequestException:
        return []
