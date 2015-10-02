from django.utils import timezone

from .models import Article, Comment

def latest_content(request):
    latest_articles = Article.objects.filter(pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
    latest_comments = Comment.objects.filter(pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
    return {'latest_articles': latest_articles,
            'latest_comments': latest_comments,
    }

