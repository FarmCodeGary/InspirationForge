from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, View, FormView
from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse

from .models import Article, Tag, Category
from .forms import CommentForm

class IndexView(ListView):
    """
    View for listing published blog posts. This view can be used by itself
    as the blog's main index, subclasses can overrride `get_queryset`,
    `get_page_title` and `get_page_heading` to show a certain subset of
    articles (e.g. a tag, an author, or a category).
    """
    template_name = 'blog/index.html'
    paginate_by = 5
    paginate_orphans = 1
    
    def get_queryset(self):
        """
        Returns queryset containing all published articles.
        """
        return Article.published_articles()
    
    def get_context_data(self, **kwargs):
        """
        Adds `page_title` and `page_heading` to the template context
        (obtained by calling `get_page_title` and `get_page_heading`,
        respectively).
        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.get_page_title()
        context['page_heading'] = self.get_page_heading()
        context['page_description'] = self.get_page_description()
        context['page_url_prefix'] = self.get_page_url_prefix()
        return context
    
    def get_page_title(self):
        """
        Returns None. (This can be overridden in a subclass to give the page
        a specific HTML title. The actual title will still include the
        site's title.)
        """
        return None
    
    def get_page_heading(self):
        """
        Returns None. (This can be overridden in a subclass to give the page
        a specific heading.)
        """
        return None
    
    def get_page_description(self):
        """
        Returns None. This can be overridden by a subclass to give the page
        a description, appearing on each page after the heading and before
        the items.
        """
        return None
    
    def get_page_url_prefix(self):
        return reverse("blog:index") + "page/"


class TagView(IndexView):
    """
    A list view that displays all published blog posts with a given tag.
    """
    
    def get_queryset(self):
        """
        Uses a keyword argument `slug` to choose a tag, and gets all
        published articles with the tag.
        """
        slug = self.kwargs['slug']
        self.tag = Tag.objects.get(slug__exact=slug)
        return Article.published_articles().filter(tags=self.tag)
    
    def get_page_title(self):
        return 'Posts tagged "{}"'.format(self.tag.name)
    
    def get_page_heading(self):
        return 'Posts tagged "{}"'.format(self.tag.name)
    
    def get_page_url_prefix(self):
        return self.tag.get_absolute_url() + "page/"


class CategoryView(IndexView):
    """
    A list view that displays all published blog posts in a given category.
    """
    
    def get_queryset(self):
        """
        Uses a keyword argument `slug` to choose a category, and gets all
        published articles in the category.
        """
        slug = self.kwargs['slug']
        self.category = Category.objects.get(slug__exact=slug)
        return Article.published_articles().filter(category=self.category)
    
    def get_page_title(self):
        return self.category.name
    
    def get_page_heading(self):
        title = self.category.title
        if title:
            return title
        else:
            return 'Category: {}'.format(self.category.name)
    
    def get_page_description(self):
        description = self.category.description
        if description:
            return description
        else:
            return super().get_page_description()
    
    def get_page_url_prefix(self):
        return self.category.get_absolute_url() + "page/"


class ArticleView(DetailView):
    """
    `DetailView` displaying the whole text of an article, plus a Comments
    section.
    """
    model = Article
    template_name = 'blog/article.html'
    
    def get_object(self):
        """
        Uses keyword arguments `year`, `month` and `slug` to find the correct
        blog article to display.
        """
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        slug = self.kwargs['slug']
        return Article.objects.get(
            pub_date__year = year,
            pub_date__month = month,
            slug__exact = slug
        )
    
    def get_context_data(self, **kwargs):
        """
        Adds a blank `CommentForm` to a context variable named `form`.
        """
        context = super(DetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context
    
    def post(self, request, *args, **kwargs):
        """
        A `POST` request is used to submit a comment on the given article.
        If the comment is successfully posted, redirect to the same page
        but with a bookmark to the new comment. Otherwise, render the page
        with the form errors.
        """
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
            
            subject = 'New comment on "{}" from "{}"'.format(
                new_comment.article.title, new_comment.name)
            uri = request.build_absolute_uri(new_comment.get_absolute_url())
            message = '{} wrote:\n"{}"\nView on site: {}'.format(
                new_comment.name, new_comment.text, uri)
            
            mail_admins(subject, message)
            return HttpResponseRedirect(new_comment.get_absolute_url())

