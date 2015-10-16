import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Article
from .feeds import LatestArticlesFeed

class LatestArticlesFeedTests(TestCase):
    def test_one_published_article_in_feed(self):
        article = Article.objects.create(title="Test article",
            source_text = "This is a test.", pub_date=timezone.now())
        feed = LatestArticlesFeed()
        self.assertQuerysetEqual(feed.items(), [repr(article)])
    
    def test_future_article_not_in_feed(self):
        time = timezone.now() + datetime.timedelta(days=1)
        article = Article.objects.create(title="Test article",
            source_text = "This is a test.", pub_date=time)
        feed = LatestArticlesFeed()
        self.assertQuerysetEqual(feed.items(), [])

