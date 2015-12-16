from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

import markdown

DEFAULT_CATEGORY_ID = 1

class Category(models.Model):
    """
    Django model representing a Category for a blog article.
    """
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True)
    
    class Meta:
        verbose_name_plural = "categories"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:category', args=[self.slug])
    
    def save(self, *args, **kwargs):
        """
        Before saving to the database, automatically generates a slug (if
        one was not given).
        """
        if self.slug == None or self.slug == "":
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """
    Django model representing a Tag (used for tagging blog posts with a
    short phrase).
    """
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:tag', args=[self.slug])
    
    def save(self, *args, **kwargs):
        """
        Before saving to the database, automatically generates a slug (if
        one was not given).
        """
        if self.slug == None or self.slug == "":
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Contributor(models.Model):
    """
    Django model representing a contributor (writer, podcast host/guest, etc.)
    """
    display_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    user = models.ForeignKey(User, blank=True, null=True)
    
    def __str__(self):
        return self.display_name
    
    def get_absolute_url(self):
        return reverse('blog:contributor', args=[self.slug])
    
    def save(self, *args, **kwargs):
        """
        Before saving to the database, automatically generates a slug (if
        one was not given).
        """
        if self.slug == None or self.slug == "":
            self.slug = slugify(self.display_name)
        super().save(*args, **kwargs)


class Article(models.Model):
    """
    Django model representing articles (posts) on the blog.
    
    The blog's `source_text` is its text in Markdown format.
    """
    MIME_TYPE_CHOICES = (
        ('audio/mpeg', 'audio/mpeg (e.g. MP3)'),
    )
    
    title = models.CharField(max_length=100)
    source_text = models.TextField()
    text = models.TextField(editable=False)
    slug = models.SlugField(max_length=100, unique_for_month='pub_date')
    pub_date = models.DateTimeField('date published', default=timezone.now)
    category = models.ForeignKey(Category, default=DEFAULT_CATEGORY_ID)
    tags = models.ManyToManyField(Tag, blank=True)
    enclosure_url = models.URLField(blank=True)
    enclosure_length = models.BigIntegerField(blank=True, null=True)
    enclosure_mime_type = models.CharField(max_length=50,
        choices=MIME_TYPE_CHOICES, blank=True)
    
    class Meta:
        ordering = ['-pub_date']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """
        URL with the year, the 2-digit month, and the article slug.
        (The specific format is determined in urls.py.)
        """
        return reverse('blog:article', args=[self.pub_date.year,
            "{:02d}".format(self.pub_date.month), self.slug])
    
    def save(self, *args, **kwargs):
        """
        Before saving, populates the `text` field with HTML generated from the
        Markdown in the `source_text`.
        """
        html = markdown.markdown(self.source_text)
        self.text = html
        if self.slug == None or self.slug == "":
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @staticmethod
    def published_articles():
        """
        Returns a QuerySet containing all published articles. An article is
        considered published if its `pub_date` is not in the the future.
        """
        return Article.objects.filter(pub_date__lte=timezone.now()
            ).order_by('-pub_date')


class Comment(models.Model):
    """"
    Django model for a comment on a blog article.
    """
    article = models.ForeignKey(Article)
    name = models.CharField(max_length=30)
    text = models.TextField(verbose_name="Comment")
    pub_date = models.DateTimeField('date published', default=timezone.now)
    
    class Meta:
        ordering = ['-pub_date']
    
    def __str__(self):
        return '{} on "{}"'.format(self.name, self.article.title)
    
    def get_absolute_url(self):
        return self.article.get_absolute_url() + "#comment-" + str(self.pk)


def image_filename(instance, filename):
    """
    Generates a filename for storing an image by converting the existing
    filename to lowercase, converting spaces and underscores to hyphens,
    and putting it in a subfolder {4-digit year}/{2-digit month} based on
    the current date.
    """
    now = timezone.now()
    reformatted = filename.lower().replace(" ","-").replace("_","-")
    return "{}/{:02d}/{}".format(now.year, now.month, reformatted)


class Image(models.Model):
    """
    Django model representing an uploaded Image.
    """
    name = models.CharField(max_length=50)
    media_file = models.ImageField(upload_to=image_filename)
    
    def __str__(self):
        return self.name

