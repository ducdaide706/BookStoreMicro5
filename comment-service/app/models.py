from django.db import models

class Comment(models.Model):
    book_id = models.IntegerField()
    content = models.TextField()
    star = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Book {self.book_id} - {self.star}⭐"
