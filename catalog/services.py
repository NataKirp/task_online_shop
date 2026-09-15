from django.core.cache import cache

from catalog.models import Product
from config.settings import CACHE_ENABLED


def get_product_by_category(category_name):
    """Возвращает список всех продуктов в указанной категории с оптимизацией запросов."""
    if not CACHE_ENABLED:
        return Product.objects.filter(category__name=category_name).select_related('category')
    # Делаем ключ уникальным для каждой категории
    key = f'products_list_{category_name}'
    filtered_products = cache.get(key)
    if filtered_products is not None:
        return filtered_products
    filtered_products = Product.objects.filter(category__name=category_name).select_related('category')
    cache.set(key, filtered_products, timeout=60)
    return filtered_products
