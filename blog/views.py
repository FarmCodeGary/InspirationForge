from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormMixin
from django.utils import timezone

from .models import Article
from .forms import CommentForm

class IndexView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_article_list'

    def get_queryset(self):
        return Article.objects.filter(pub_date__lte=timezone.now()
            ).order_by('-pub_date')[:5]

class ArticleView(FormMixin, DetailView):
    model = Article
    template_name = 'blog/article.html'
    form_class = CommentForm
    
    def get_object(self):
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        slug = self.kwargs['slug']
        return Article.objects.get(
            pub_date__year = year,
            pub_date__month = month,
            slug__exact = slug
        )
    
    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self, form):
        # Post the comment?
        return super(AuthorDetail, self).form_valid(form)

