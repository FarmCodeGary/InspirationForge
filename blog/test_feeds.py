import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Article
from .feeds import LatestArticlesFeed


class LatestArticlesFeedTests(TestCase):
    def test_one_published_article_in_feed(self):
        article = Article.objects.create(
            title="Test article",
            content_source="This is a test.",
            pub_date=timezone.now())
        feed = LatestArticlesFeed()
        self.assertQuerysetEqual(feed.items(), [repr(article)])

    def test_future_article_not_in_feed(self):
        time = timezone.now() + datetime.timedelta(days=1)
        Article.objects.create(
            title="Test article",
            content_source="This is a test.",
            pub_date=time)
        feed = LatestArticlesFeed()
        self.assertQuerysetEqual(feed.items(), [])

    def test_article_content_in_feed(self):
        Article.objects.create(
            title="Test article",
            content_source="This is a test.",
            pub_date=timezone.now())
        response = self.client.get(reverse('blog:rssfeed'))
        self.assertContains(response, "This is a test.")
        self.assertContains(response, "Test article")
