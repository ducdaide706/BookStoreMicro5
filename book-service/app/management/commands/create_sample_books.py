from django.core.management.base import BaseCommand
from app.models import Book


class Command(BaseCommand):
    help = 'Create sample books'

    def handle(self, *args, **kwargs):
        books_data = [
            {
                'title': 'Clean Code',
                'author': 'Robert C. Martin',
                'price': 350000,
                'description': 'Hướng dẫn viết code sạch và dễ bảo trì',
                'stock': 10
            },
            {
                'title': 'Design Patterns',
                'author': 'Gang of Four',
                'price': 450000,
                'description': 'Các mẫu thiết kế phần mềm kinh điển',
                'stock': 8
            },
            {
                'title': 'The Pragmatic Programmer',
                'author': 'Andrew Hunt & David Thomas',
                'price': 400000,
                'description': 'From Journeyman to Master',
                'stock': 15
            },
            {
                'title': 'Head First Design Patterns',
                'author': 'Eric Freeman',
                'price': 380000,
                'description': 'A Brain-Friendly Guide',
                'stock': 12
            },
            {
                'title': 'Refactoring',
                'author': 'Martin Fowler',
                'price': 420000,
                'description': 'Improving the Design of Existing Code',
                'stock': 7
            },
            {
                'title': 'Microservices Patterns',
                'author': 'Chris Richardson',
                'price': 480000,
                'description': 'With examples in Java',
                'stock': 5
            },
        ]
        
        for book_data in books_data:
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults=book_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created book: {book.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Book already exists: {book.title}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nTotal books: {Book.objects.count()}')
        )
