import os.path

from django.test import TestCase

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

