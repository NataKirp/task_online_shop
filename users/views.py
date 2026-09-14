from django.contrib.auth import login
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from config import settings
from users.forms import UserRegisterForm


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_email(user.email)
        # Автоматически логиним пользователя на сайте
        # Параметр backend указывать обязательно, чтобы Django знал, через какую систему авторизовать
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать на сайт "Мой сад"!'
        message = 'Поздравляем с успешной регистрацией!'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user_email, ]
        send_mail(subject, message, from_email, recipient_list)
