from django.db import models

class Catalog(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class CatalogBook(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    book_id = models.IntegerField()