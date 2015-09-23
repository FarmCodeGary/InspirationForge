from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Article

class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_article_list'

    def get_queryset(self):
        return Article.objects.order_by('-pub_date')[:5]

class ArticleView (generic.DetailView):
    model = Article
    template_name = 'blog/article.html'

def test(request):
    return render(request, 'base.html', {})
