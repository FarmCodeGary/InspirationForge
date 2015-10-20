from django.utils import timezone
from django.db.models import Count

from .models import Article, Comment, Tag

def latest_content(request):
    """
    Adds 5 latest blog posts as `latest_articles`, 5 latest comments as
    `latest_comments`, and all tags (annotated with `num_articles` field) as
    `tags` to the context, regardless of `request`.
    """
    latest_articles = Article.objects.filter(pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
    latest_comments = Comment.objects.filter(pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
    tags = Tag.objects.annotate(num_articles=Count('article')).order_by(
        '-num_articles')
    return {'latest_articles': latest_articles,
            'latest_comments': latest_comments,
            'tags': tags,
    }

