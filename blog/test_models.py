"""
Unit tests for the blog app's Django models.
"""


import os.path, datetime

from django.test import TestCase
from django.utils import timezone

from .models import Article, image_filename

class ArticleMethodTests(TestCase):
    """
    Tests for methods of the Article model.
    """
    
    def test_save_generates_html(self):
        """
        save() should populate the article's text field with HTML.
        """
        content_source = "Test post text"
        article = Article(title="test article", content_source=content_source)
        article.save()
        self.assertEqual(article.rendered_content.strip(),
            "<p>Test post text</p>"
        )
    
    
    def test_published_articles(self):
        """
        published_articles() should include only articles with a pub_date in
        the past, with the most recent articles first.
        """
        Article.objects.create(title="Past Article",
            content_source="test",
            pub_date=(timezone.now() + datetime.timedelta(days=-1)))
        Article.objects.create(title="Future Article",
            content_source="test",
            pub_date=(timezone.now() + datetime.timedelta(days=1)))
        Article.objects.create(title="Current Article",
            content_source="test",
            pub_date=timezone.now())
        self.assertQuerysetEqual(Article.published_articles(),
            ['<Article: Current Article>', '<Article: Past Article>'])


class ImageFilenameTests(TestCase):
    """
    Tests for fixing the filenames of images.
    """
    
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

