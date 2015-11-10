import os.path, datetime

from django.test import TestCase
from django.utils import timezone

from .models import Article, image_filename

class ArticleMethodTests(TestCase):
    def test_save_generates_html(self):
        """
        save() should populate the article's text field with HTML.
        """
        source_text = "Test post text"
        article = Article(title="test article", source_text=source_text)
        article.save()
        self.assertEqual(article.text.strip(), "<p>Test post text</p>")
    
    
    def test_published_articles(self):
        """
        published_articles() should include only articles with a pub_date in
        the past, with the most recent articles first.
        """
        past_article = Article.objects.create(title="Past Article",
            source_text="test",
            pub_date=(timezone.now() + datetime.timedelta(days=-1)))
        future_article = Article.objects.create(title="Future Article",
            source_text="test",
            pub_date=(timezone.now() + datetime.timedelta(days=1)))
        current_article = Article.objects.create(title="Current Article",
            source_text="test",
            pub_date=timezone.now())
        self.assertQuerysetEqual(Article.published_articles(),
            ['<Article: Current Article>', '<Article: Past Article>'])


class ImageFilenameTests(TestCase):
    def test_with_spaces(self):
        """
        image_filename should convert spaces to hyphens.
        """
        original = "test image.png"
        result = image_filename(None, original) # The instance shouldn't matter
        self.assertEqual(os.path.basename(result), "test-image.png")
    
    def test_with_underscores(self):
        """
        image_filename should convert underscores to hyphens.
        """
        original = "test_image.png"
        result = image_filename(None, original) # The instance shouldn't matter
        self.assertEqual(os.path.basename(result), "test-image.png")

