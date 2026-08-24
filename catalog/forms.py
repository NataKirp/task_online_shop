import re

from django import forms
from django.forms import BooleanField

from catalog.constants import BLACKLIST
from catalog.models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    new_category_name = forms.CharField(
        max_length=50,
        required=False,
        label='Наименование',
        help_text='Заполните, если в списке нет нужной категории'
    )
    new_category_description = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label='Описание',
        help_text='Введите описание новой категории'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'

            if self.errors and field_name in self.errors:
                field.widget.attrs['class'] += ' is-invalid'

    def _validate_blacklist(self, text):
        """Служебный метод для поиска запрещенных слов в тексте."""
        text_lower = text.lower()
        found_words = []

        for forbidden_word in BLACKLIST:
            # Ищем точное совпадение слова целиком с помощью \b
            pattern = rf'\b{re.escape(forbidden_word)}\b'
            if re.search(pattern, text_lower):
                found_words.append(forbidden_word)

        if found_words:
            words_str = ", ".join([f'"{w}"' for w in found_words])
            raise forms.ValidationError(f'{words_str} нельзя использовать!')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        self._validate_blacklist(name)
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        self._validate_blacklist(description)
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной!')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.content_type not in ['image/jpeg', 'image/png']:
                raise forms.ValidationError('Формат изображения должен быть JPEG или PNG.')
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Размер изображения не должен превышать 5 МБ.')
        return image

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        new_category_name = cleaned_data.get('new_category_name')

        if not category and not new_category_name:
            raise forms.ValidationError('Выберите существующую категорию или укажите название для новой.')

        if new_category_name and Category.objects.filter(name=new_category_name).exists():
            raise forms.ValidationError(
                {
                    'new_category_name': f'Категория с названием "{new_category_name}" уже существует. Выберите её из списка.'}
            )
        return cleaned_data
