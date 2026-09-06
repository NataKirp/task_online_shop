from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from config import settings
from users.forms import UserRegisterForm


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать на сайт "Мой сад"!'
        message = 'Поздравляем с успешной регистрацией!'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user_email, ]
        send_mail(subject, message, from_email, recipient_list)
