import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Article
from .views import ArticleView, IndexView

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

class IndexViewTests(TestCase):
    def test_with_a_future_article(self):
        """
        Articles with a pub_date in the future should not be displayed on the
        index page.
        """
        create_article("Future article",days_in_past=-1)
        response = self.client.get(reverse('blog:index'))
        self.assertContains(response, 'No posts are available.',
                            status_code=200)
        self.assertQuerysetEqual(response.context['latest_article_list'], [])

class ArticleViewTests(TestCase):
    def test_without_leading_zero_on_month(self):
        pub_date = datetime.datetime(2013, 9, 15)
        article = Article.objects.create(title="testarticle", source_text="testbody",
            pub_date=pub_date)
        response = self.client.get(reverse('blog:article',
            args=['2013','9','testarticle']))
        self.assertContains(response, 'testarticle', status_code=200)
        self.assertContains(response, 'testbody')


