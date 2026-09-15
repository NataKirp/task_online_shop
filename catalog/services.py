from catalog.models import Product


def get_product_by_category(category_name):
    """Возвращает список всех продуктов в указанной категории с оптимизацией запросов."""
    return Product.objects.filter(category__name=category_name).select_related('category')
