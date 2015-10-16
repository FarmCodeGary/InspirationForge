import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Article, Comment
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
        self.assertQuerysetEqual(response.context['article_list'], [])


class ArticleViewTests(TestCase):
    def test_without_leading_zero_on_month(self):
        pub_date = timezone.make_aware(datetime.datetime(2013, 9, 15))
        article = Article.objects.create(title="testarticle", source_text="testbody",
            pub_date=pub_date)
        response = self.client.get(reverse('blog:article',
            args=['2013','9','testarticle']))
        self.assertContains(response, 'testarticle', status_code=200)
        self.assertContains(response, 'testbody')
    
    def test_post_valid_comment(self):
        """
        Posting a comment with name and text should work.
        """
        article = Article.objects.create(title="testarticle")
        response = self.client.post(
            article.get_absolute_url() + "#commentform",
            { 'name': 'John', 'text': 'Test comment!' },
            follow = True,
        )
        self.assertContains(response, 'Test comment!', status_code=200)
        self.assertContains(response, 'John')
    
    def test_post_comment_without_text(self):
        """
        Posting a comment without text should not post the comment and
        should instead display an error message.
        """
        article = Article.objects.create(title="testarticle")
        response = self.client.post(
            article.get_absolute_url() + "#commentform",
            { 'name': 'John', 'text': '' },
            follow = True,
        )
        self.assertContains(response, 'John')
        self.assertContains(response, 'This field is required.')
    
    def test_post_comment_without_name(self):
        """
        Posting a comment without a name should not post the comment and should
        instead display an error message.
        """
        article = Article.objects.create(title="testarticle")
        response = self.client.post(
            article.get_absolute_url() + "#commentform",
            { 'name': '', 'text': 'Test comment!' },
            follow = True,
        )
        self.assertContains(response, 'Test comment!')
        self.assertContains(response, 'This field is required.')
    
