from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.http import HttpResponseRedirect, Http404
from django.core.mail import mail_admins
from django.core.urlresolvers import reverse

from .models import Article, Tag, Category, Contributor
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
        context['page_url_prefix'] = self.get_page_url_prefix()
        return context

    def get_page_url_prefix(self):
        return reverse("blog:index") + "page/"


class TagView(IndexView):
    """
    A list view that displays all published blog posts with a given tag.
    """

    template_name = 'blog/tag.html'

    def get_queryset(self):
        """
        Uses a keyword argument `slug` to choose a tag, and gets all
        published articles with the tag.
        """
        slug = self.kwargs['slug']
        self.tag = Tag.objects.get(slug__exact=slug)
        return Article.published_articles().filter(tags=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context

    def get_page_url_prefix(self):
        return self.tag.get_absolute_url() + "page/"


class CategoryView(IndexView):
    """
    A list view that displays all published blog posts in a given category.
    """

    template_name = 'blog/category.html'

    def get_queryset(self):
        """
        Uses a keyword argument `slug` to choose a category, and gets all
        published articles in the category.
        """
        slug = self.kwargs['slug']
        try:
            self.category = Category.objects.get(slug__exact=slug)
        except Category.DoesNotExist:
            raise Http404(
                "Tried and failed to find category with slug '{}'."
                .format(slug)
            )
        else:
            return Article.published_articles().filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

    def get_page_url_prefix(self):
        return self.category.get_absolute_url() + "page/"


class ContributorView(IndexView):

    template_name = 'blog/contributor.html'

    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            self.contributor = Contributor.objects.get(
                slug__exact=slug
            )
        except Contributor.DoesNotExist:
            raise Http404("Failed to find contributor with slug '{}'."
                          .format(slug))
        else:
            return Article.published_articles().filter(
                contributors=self.contributor
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contributor'] = self.contributor
        return context

    def get_page_url_prefix(self):
        return self.contributor.get_absolute_url() + "page/"


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
        try:
            article = Article.objects.get(
                pub_date__year=year,
                pub_date__month=month,
                slug__exact=slug
            )
        except Article.DoesNotExist:
            raise Http404("Failed to find article with year {}, month {}, " +
                          "and slug '{}'.".format(year, month, slug))
        return article

    def get_context_data(self, **kwargs):
        """
        Adds a blank `CommentForm` to a context variable named `form`.
        """
        context = super(DetailView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
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
