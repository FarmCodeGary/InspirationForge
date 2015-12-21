"""
Context processors for the blog app.
"""

from django.db.models import Count

from .models import Article, Comment, Tag, Contributor


def latest_content(request):
    """
    Adds 5 latest blog posts as `latest_articles`, 5 latest comments as
    `latest_comments`, and all tags (annotated with `num_articles` field) as
    `tags` to the context, regardless of `request`.
    """
    latest_articles = Article.published_articles()[:5]
    latest_comments = Comment.objects.all().order_by('-pub_date')[:5]
    tags = Tag.objects.annotate(num_articles=Count('article')).order_by(
        '-num_articles')
    contributors = Contributor.objects.annotate(
        num_articles=Count('article')).order_by('-num_articles')
    return {'latest_articles': latest_articles,
            'latest_comments': latest_comments,
            'tags': tags,
            'contributors': contributors,
            }
