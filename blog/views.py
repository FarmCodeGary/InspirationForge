from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.utils import timezone

from .models import Article

class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_article_list'

    def get_queryset(self):
        return Article.objects.filter(pub_date__lte=timezone.now()
            ).order_by('-pub_date')[:5]

class ArticleView (generic.DetailView):
    model = Article
    template_name = 'blog/article.html'
    
    def get_object(self):
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        slug = self.kwargs['slug']
        return Article.objects.get(
            pub_date__year = year,
            pub_date__month = month,
            slug__exact = slug)

