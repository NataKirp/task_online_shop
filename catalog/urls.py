from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductDetailView, ProductListView, ContactsTemplateView, ProductCreateView, \
    ProductUpdateView, ProductDeleteView, ProductUnpublishView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='list'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:pk>/unpublish/', ProductUnpublishView.as_view(), name='product_unpublish'),
]
