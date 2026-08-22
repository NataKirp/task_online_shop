from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Product, Category


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(CreateView):
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

        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list')

    def get_success_url(self):
        return reverse('catalog:product_detail', args=[self.kwargs.get('pk')])


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:list')


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
