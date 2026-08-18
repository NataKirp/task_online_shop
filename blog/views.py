from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Article


class ArticleListView(ListView):
    model = Article
    context_object_name = 'articles'

class ArticleDetailView(DetailView):
    model = Article

class ArticleCreateView(CreateView):
    model = Article
    fields = ("title", "content", "preview", "publication_date")
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        article = form.save(commit=False)

        if 'publish' in self.request.POST:
            article.is_published = True
            if not article.publication_date:
                article.publication_date = timezone.now().date()

        elif 'save_draft' in self.request.POST:
            article.is_published = False
            article.publication_date = None

        article.save()
        return super().form_valid(form)

class ArticleUpdateView(UpdateView):
    model = Article
    fields = ("title", "content", "preview", "publication_date")
    success_url = reverse_lazy('blog:list')


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('blog:list')