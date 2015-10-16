from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, View, FormView
from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator

from .models import Article, Tag
from .forms import CommentForm

class IndexView(ListView):
    template_name = 'blog/index.html'
    paginate_by = 5
    paginate_orphans = 1
    queryset = Article.published_articles()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = self.get_page_title()
        context['page_title'] = self.get_page_title()
        context['page_heading'] = self.get_page_heading()
        return context
    
    def get_page_title(self):
        return None
    
    def get_page_heading(self):
        return None


class TagView(IndexView):
    def get_queryset(self):
        slug = self.kwargs['slug']
        return Article.published_articles().filter(tags__slug__exact=slug)
    
    def get_page_title(self):
        tag = Tag.objects.get(slug__exact=self.kwargs['slug'])
        return 'Posts tagged "{}"'.format(tag.name)
    
    def get_page_heading(self):
        tag = Tag.objects.get(slug__exact=self.kwargs['slug'])
        return 'Posts tagged "{}"'.format(tag.name)


class ArticleView(DetailView):
    model = Article
    template_name = 'blog/article.html'
    
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
        context['form'] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        try:
            new_comment = form.save(commit=False)
        except ValueError:
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)
        else:
            new_comment.article = self.object
            new_comment.pub_date = timezone.now()
            new_comment.save()
            return HttpResponseRedirect(new_comment.get_absolute_url())

