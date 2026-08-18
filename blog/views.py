from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Article


class ArticleListView(ListView):
    model = Article
    context_object_name = 'articles'

    def get_queryset(self):
        queryset = super().get_queryset()
        current_date = timezone.now().date()
        return queryset.filter(is_published=True, publication_date__lte=current_date).order_by('-publication_date')


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


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

    def get_success_url(self):
        return reverse('blog:article_detail', args=[self.kwargs.get('pk')])


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('blog:list')
