import datetime

from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import timezone

from .models import Article
from .context_processors import latest_content

def create_article(title, source_text="test article text", days_in_past=0):
    """
    Creates an article with the given title and optionally the given text and
    number of days in the past. (Use a negative value for `days_in_past` to
    indicate a date in the future.) If `days_in_past` is not set, the article
    will have the default datetime of timezone.now().
    """
    time = timezone.now() + datetime.timedelta(days=-days_in_past)
    return Article.objects.create(title=title, source_text=source_text,
                                  pub_date = time)

class LatestContentTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_latest_articles_with_no_articles(self):
        """
        When there are no articles, `latest_articles` should be empty.
        """
        request = self.factory.get('/')
        context = latest_content(request)
        self.assertQuerysetEqual(context['latest_articles'], [])
    
    def test_latest_articles_with_future_article(self):
        """
        When there's only one article -- which is in the future --
        `latest_articles` should be empty.
        """
        create_article("article 1", days_in_past = -1)
        request = self.factory.get('/')
        context = latest_content(request)
        self.assertQuerysetEqual(context['latest_articles'], [])
    
    def test_latest_articles_with_past_article(self):
        create_article("article 1", days_in_past = 1)
        request = self.factory.get('/')
        context = latest_content(request)
        self.assertQuerysetEqual(context['latest_articles'],
            ['<Article: article 1>']
        )

