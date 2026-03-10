from django.contrib import admin
from .models import Catalog, CatalogBook

admin.site.register(Catalog)
admin.site.register(CatalogBook)

class CatalogAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')