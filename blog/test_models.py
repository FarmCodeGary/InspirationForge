from django.test import TestCase

from .models import Article

class ArticleMethodTests(TestCase):
    def test_save_generates_html(self):
        """
        save() should populate the article's text field with HTML.
        """
        source_text = "Test post text"
        article = Article(title="test article",source_text=source_text)
        article.save()
        self.assertEqual(article.text.strip(),"<p>Test post text</p>")

