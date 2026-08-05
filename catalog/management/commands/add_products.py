from django.core.management import BaseCommand, call_command
from django.core.management.color import color_style
from catalog.models import Product


class Command(BaseCommand):
    help = 'Добавление тестового продукта в базу данных из фикстуры'

    def handle(self, *args, **options):
        self.style = color_style(force_color=True)

        deleted_count, _ = Product.objects.all().delete()
        self.stdout.write(self.style.WARNING(f'Существующие данные удалены из базы. Удалено {deleted_count} объектов'))

        call_command('loaddata', 'products_fixture.json')
        self.stdout.write(self.style.SUCCESS('Данные успешно загружены из фикстуры'))