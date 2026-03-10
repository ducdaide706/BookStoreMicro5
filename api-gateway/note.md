
cd customer-service
python manage.py runserver 8001
cd..
cd api-gateway
python manage.py runserver 8000
cd..
cd cart-service
python manage.py migrate
python manage.py runserver 8002
cd..
