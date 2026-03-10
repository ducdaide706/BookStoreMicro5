from django.db import models
from django.contrib.auth.hashers import make_password

class Staff(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    @staticmethod
    def create_root():
        if not Staff.objects.filter(username='duc').exists():
            Staff.objects.create(
                username='duc',
                password=make_password('123456'),
                name='Duc',
                email='duc@example.com'
            )
