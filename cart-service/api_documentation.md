# Cart Service Documentation

## Endpoints

- `/api/carts/customer/<customer_id>/` (GET): Lấy giỏ hàng theo customer
- `/api/carts/` (POST): Tạo giỏ hàng
- `/api/carts/<cart_id>/add-item/` (POST): Thêm sách vào giỏ
- `/api/carts/<cart_id>/remove-item/<item_id>/` (DELETE): Xóa sách khỏi giỏ

## Notes
- Quản lý giỏ hàng, item, quantity.
