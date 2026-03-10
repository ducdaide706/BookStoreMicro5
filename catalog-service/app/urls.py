from django.urls import path
from .views import CatalogListView, CatalogBookListView

urlpatterns = [
    path('catalogs/', CatalogListView.as_view(), name='catalog-list'),
    path('catalog_books/', CatalogBookListView.as_view(), name='catalogbook-list'),
]