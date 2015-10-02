from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, View, FormView
from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin
from django.utils import timezone
from django.http import HttpResponseRedirect

from .models import Article
from .forms import CommentForm

class IndexView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_article_list'

    def get_queryset(self):
        return Article.objects.filter(pub_date__lte=timezone.now()
            ).order_by('-pub_date')[:5]

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

