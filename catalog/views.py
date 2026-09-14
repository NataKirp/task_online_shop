from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Product, Category


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser or (
                user.is_authenticated and user.groups.filter(name__in=['Продавцы', 'Модераторы продуктов']).exists()):
            return Product.objects.all()
        return Product.objects.filter(is_published=True)


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list')

    def form_valid(self, form):
        new_category_name = form.cleaned_data.get('new_category_name')
        new_category_description = form.cleaned_data.get('new_category_description')

        # Если пользователь решил создать новую категорию
        if new_category_name:
            # Создаем и сохраняем новую категорию в БД
            new_category = Category.objects.create(
                name=new_category_name,
                description=new_category_description
            )
            # Привязываем свежесозданную категорию к объекту продукта
            form.instance.category = new_category

        product = form.save(commit=False)

        product.owner = self.request.user

        # Обработка кнопки "Опубликовать товар"
        if 'publish' in self.request.POST:
            product.is_published = True
            if product.status == 'draft':
                product.status = 'active'

        product.save()
        return redirect('catalog:list')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list')

    def get_object(self, queryset=None):
        product = super().get_object(queryset)
        if self.request.user == product.owner or self.request.user.is_superuser:
            return product
        raise PermissionDenied("Вы не можете редактировать этот товар, т.к. не являетесь его владельцем.")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        old_product = self.get_object()
        product = form.save(commit=False)

        # Если товар уже был в продаже, удерживаем флаг публикации при сохранении
        if old_product.is_published:
            product.is_published = True

        # Если черновик публикуется продавцом впервые через специальную кнопку
        if 'publish' in self.request.POST:
            product.is_published = True
            if product.status == 'draft':
                product.status = 'active'

        # Если товар УЖЕ БЫЛ опубликован, и продавец НЕ выбрал статусы
        # проблем с наличием ('out_of-stock' или 'discontinued') — принудительно держим статус 'active'
        elif old_product.is_published:
            if product.status == 'draft' or not product.status:
                product.status = 'active'

        product.save()
        return redirect('catalog:list')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:list')

    def dispatch(self, request, *args, **kwargs):
        # Сначала находим продукт в базе данных по ID из URL-адреса
        product = self.get_object()

        is_moderator = request.user.groups.filter(name='Модераторы продуктов').exists()

        if self.request.user != product.owner and not request.user.is_superuser and not is_moderator:
            raise PermissionDenied("Вы не можете удалить этот товар, т.к. не являетесь его владельцем.")

        return super().dispatch(request, *args, **kwargs)


class ProductUnpublishView(PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'
    raise_exception = True  # Выдаст 403

    def post(self, request, pk, *args, **kwargs):
        # Находим продукт по pk
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.status = 'draft'  # Возвращаем статус черновика при снятии с сайта
        product.save()
        return redirect('catalog:list')


class ContactsTemplateView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f"Новое сообщение! Имя: {name}, Телефон: {phone}. Текст: {message}")
        context = self.get_context_data(**kwargs)
        context['success'] = True
        context['user_name'] = name
        return render(request, self.template_name, context)
