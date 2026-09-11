from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Создает стандартные группы пользователей и назначает им права"

    def handle(self, *args, **options):
        GROUPS_PERMISSIONS = {
            'Продавцы': [
                'add_product',
                'change_product',
                'view_product',
                'delete_product',
            ],
            'Модераторы продуктов': [
                'view_product',
                'delete_product',
                'can_unpublish_product'
            ],
            'Авторы': [
                'add_article',
                'change_article',
                'view_article',
                'delete_article',
            ],
            'Контент-менеджеры': [
                'add_article',
                'change_article',
                'view_article',
                'delete_article',
            ]
        }

        self.stdout.write(self.style.WARNING('--- Создание групп и назначение прав ---'))

        for group_name, perm_codename_list in GROUPS_PERMISSIONS.items():
            group, created = Group.objects.get_or_create(name=group_name)

            if created:
                self.stdout.write(self.style.SUCCESS(f'Создана группа: "{group_name}"'))
            else:
                self.stdout.write(self.style.NOTICE(f'Группа: "{group_name}" уже существует. Обновляем права...'))

            permissions_to_add = []

            for codename in perm_codename_list:
                try:
                    permission = Permission.objects.get(codename=codename)
                    permissions_to_add.append(permission)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Ошибка: право "{codename}" не найдено!'))

            if permissions_to_add:
                group.permissions.set(permissions_to_add)
                self.stdout.write(self.style.SUCCESS(f'Для "{group_name}" назначено "{len(permissions_to_add)}" прав.'))

        self.stdout.write(self.style.SUCCESS('--- Настройка групп успешно завершена! ---'))