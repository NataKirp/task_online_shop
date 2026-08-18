from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductDetailView, ProductListVieW, ContactsTemplateView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListVieW.as_view(), name='list'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]
