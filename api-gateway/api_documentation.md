# API Gateway Documentation

## Endpoints

- `/` (GET): Trang chủ
- `/register/` (POST): Đăng ký khách hàng
- `/login/` (POST): Đăng nhập khách hàng
- `/staff/login/` (POST): Đăng nhập staff
- `/staff/customers/` (GET): Danh sách customer cho staff
- `/staff/add-book/` (POST): Staff thêm sách
- `/books/` (GET): Danh sách sách theo catalog
- `/cart/` (GET): Xem giỏ hàng
- `/cart/add/` (POST): Thêm sách vào giỏ
- `/cart/<cart_id>/remove/<item_id>/` (POST): Xóa sách khỏi giỏ
- `/books/<book_id>/` (GET): Xem chi tiết sách
- `/books/<book_id>/add_comment/` (POST): Đánh giá sách
- `/cart/checkout/` (POST): Thanh toán, tạo order
- `/pay/` (GET/POST): Chọn phương pháp trả, trả tiền, tạo shipment
- `/orders/` (GET): Danh sách đơn hàng đã đặt
- `/pay/methods/` (GET): Lấy danh sách phương pháp trả

## Notes
- Tích hợp nhiều service, chuyển tiếp request, render template, xử lý logic tổng hợp.
- CSRF bảo vệ cho các form POST.
- Gọi các service qua HTTP API.
