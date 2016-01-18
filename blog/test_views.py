import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Article, Tag


def create_article(title, content_source="test article text", days_in_past=0):
    """
    Creates an article with the given title and optionally the given text and
    number of days in the past. (Use a negative value for `days_in_past` to
    indicate a date in the future.) If `days_in_past` is not set, the article
    will have the default datetime of timezone.now().
    """
    time = timezone.now() + datetime.timedelta(days=-days_in_past)
    return Article.objects.create(title=title,
                                  content_source=content_source,
                                  pub_date=time)


class IndexViewTests(TestCase):
    def test_with_a_future_article(self):
        """
        Articles with a pub_date in the future should not be displayed on the
        index page.
        """
        create_article("Future article", days_in_past=-1)
        response = self.client.get(reverse('blog:index'))
        self.assertContains(response, 'No posts are available.',
                            status_code=200)
        self.assertQuerysetEqual(response.context['article_list'], [])

    def test_with_a_past_article(self):
        """
        Articles with a pub_date in the past should be displayed on the index
        page.
        """
        article = create_article(
            "Past article",
            days_in_past=1,
            content_source="test article text")
        response = self.client.get(reverse('blog:index'))
        self.assertContains(response, "<h3>{}</h3>".format(article.title),
                            status_code=200)
        self.assertContains(response, "test article text")
        self.assertQuerysetEqual(
            response.context['article_list'],
            ['<Article: Past article>'])

    def test_with_recent_article(self):
        """
        Articles with a pub_date in the very recent past should be displayed
        on the index page.
        """
        article = create_article("Recent article", days_in_past=0)
        response = self.client.get(reverse('blog:index'))
        self.assertContains(response, "<h3>{}</h3>".format(article.title),
                            status_code=200)
        self.assertQuerysetEqual(
            response.context['article_list'],
            ['<Article: Recent article>'])


class TagViewTests(TestCase):
    def test_with_nonexistent_tag(self):
        """
        Looking for a non-existent tag should cause a 404 error.
        """
        response = self.client.get(reverse('blog:tag', args=['doesnt-exist']))
        self.assertEqual(response.status_code, 404)

    def test_with_future_article(self):
        """
        Articles with a pub_date in the future should not be displayed on the
        tag page.
        """
        tag = Tag.objects.create(name="test tag")
        article = Article.objects.create(
            title="Future article",
            content_source="This is a test article.",
            pub_date=(timezone.now() + datetime.timedelta(days=1)))
        article.tags.add(tag)
        response = self.client.get(reverse('blog:tag', args=["test-tag"]))
        self.assertContains(
            response, 'No posts are available.',
            status_code=200)
        self.assertQuerysetEqual(response.context['article_list'], [])


class CategoryViewTests(TestCase):
    def test_with_nonexistent_category(self):
        """
        Looking for a non-existent category should cause a 404 error.
        """
        response = self.client.get(reverse(
            'blog:category',
            args=['doesnt-exist']
        ))
        self.assertEqual(response.status_code, 404)


class ContributorViewTests(TestCase):
    def test_with_nonexistent_contributor(self):
        """
        Looking for a non-existent contributor should cause a 404 error.
        """
        response = self.client.get(reverse(
            'blog:category',
            args=['doesnt-exist']
        ))
        self.assertEqual(response.status_code, 404)


class ArticleViewTests(TestCase):
    def test_with_nonexistent_article(self):
        response = self.client.get(reverse(
            'blog:article',
            args=['2015', '1', 'doesnt-exist']
        ))
        self.assertEqual(response.status_code, 404)

    def test_without_leading_zero_on_month(self):
        pub_date = timezone.make_aware(datetime.datetime(2013, 9, 15))
        Article.objects.create(
            title="testarticle",
            content_source="testbody",
            pub_date=pub_date)
        response = self.client.get(reverse(
            'blog:article',
            args=['2013', '9', 'testarticle']))
        self.assertContains(response, 'testarticle', status_code=200)
        self.assertContains(response, 'testbody')

    def test_post_valid_comment(self):
        """
        Posting a comment with name and text should work.
        """
        article = Article.objects.create(title="testarticle")
        response = self.client.post(
            article.get_absolute_url() + "#commentform",
            {'name': 'John', 'text': 'Test comment!'},
            follow=True,
        )
        self.assertContains(response, '<p>Test comment!</p>', status_code=200)
        self.assertContains(response, 'John')

    def test_post_comment_without_text(self):
        """
        Posting a comment without text should not post the comment and
        should instead display an error message.
        """
        article = Article.objects.create(title="testarticle")
        response = self.client.post(
            article.get_absolute_url() + "#commentform",
            {'name': 'John', 'text': ''},
            follow=True,
        )
        self.assertContains(response, 'John')

        # Make sure "John" isn't part of a posted comment in a heading:
        self.assertNotContains(response, 'John</h3>')

        self.assertContains(response, 'This field is required.')

    def test_post_comment_without_name(self):
        """
        Posting a comment without a name should not post the comment and should
        instead display an error message.
        """
        article = Article.objects.create(title="testarticle")
        response = self.client.post(
            article.get_absolute_url() + "#commentform",
            {'name': '', 'text': 'Test comment!'},
            follow=True,
        )
        self.assertContains(response, 'Test comment!')
        self.assertNotContains(response, '<p>Test comment!</p>')
        self.assertContains(response, 'This field is required.')
