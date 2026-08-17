from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView

from catalog.models import Product


class ProductListVieW(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ContactsTemplateView(TemplateView):
    template_name ='catalog/contacts.html'


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


class ProductDetailView(DetailView):
    model = Product

