import datetime

from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import timezone

from .models import Article, Comment, Tag
from .context_processors import latest_content

def create_article(title, content_source="test article text", days_in_past=0):
    """
    Creates an article with the given title and optionally the given text and
    number of days in the past. (Use a negative value for `days_in_past` to
    indicate a date in the future.) If `days_in_past` is not set, the article
    will have the default datetime of timezone.now().
    """
    time = timezone.now() + datetime.timedelta(days=-days_in_past)
    return Article.objects.create(title=title, content_source=content_source,
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
        """
        When there's an article in the past, it should appear in the context
        variable `latest_articles`.
        """
        create_article("article 1", days_in_past = 1)
        request = self.factory.get('/')
        context = latest_content(request)
        self.assertQuerysetEqual(context['latest_articles'],
            ['<Article: article 1>']
        )
    
    def test_latest_articles_with_recent_article(self):
        """
        When there's a very recent article, it should appear in the context
        variable `latest_articles`.
        """
        create_article("article 1", days_in_past = 0)
        request = self.factory.get('/')
        context = latest_content(request)
        self.assertQuerysetEqual(context['latest_articles'],
            ['<Article: article 1>']
        )
    
    def test_latest_comments(self):
        """
        Comments should appear in the context variable `latest_comments`, the
        most recent first.
        """
        article1 = create_article("article 1")
        article2 = create_article("article 2")
        comment1 = Comment.objects.create(article=article1, name="Dennis",
            text="comment 1")
        comment2 = Comment.objects.create(article=article2, name="Dwayne",
            text="comment 2")
        comment3 = Comment.objects.create(article=article1, name="Murray",
            text="comment 3")
        request = self.factory.get('/')
        context = latest_content(request)
        self.assertQuerysetEqual(context['latest_comments'],
            ['<Comment: Murray on "article 1">',
            '<Comment: Dwayne on "article 2">',
            '<Comment: Dennis on "article 1">'])
    
    def test_tags(self):
        """
        Tags should appear in the context variable `tags`, sorted by the number
        of articles.
        """
        article1 = create_article("article 1")
        article2 = create_article("article 2")
        puppies_tag = Tag.objects.create(name="puppies", slug="puppies")
        kittens_tag = Tag.objects.create(name="kittens", slug="kittens")
        article1.tags.add(puppies_tag)
        article1.tags.add(kittens_tag)
        article2.tags.add(kittens_tag)
        
        request = self.factory.get('/')
        context = latest_content(request)
        self.assertQuerysetEqual(context['tags'],
            ['<Tag: kittens>', '<Tag: puppies>'])
        self.assertEqual(context['tags'][0].num_articles, 2)
        self.assertEqual(context['tags'][1].num_articles, 1)

