from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Article

class IndexView(generic.ListView):
    template_name = 'forgeblog/index.html'
    context_object_name = 'latest_article_list'

    def get_queryset(self):
        return Article.objects.order_by('-pub_date')[:5]

class ArticleView (generic.DetailView):
    model = Article
    template_name = 'forgeblog/article.html'
