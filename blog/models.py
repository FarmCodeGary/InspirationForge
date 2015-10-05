from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.core.urlresolvers import reverse

import markdown

class Article(models.Model):
    title = models.CharField(max_length=100)
    source_text = models.TextField()
    text = models.TextField(editable=False)
    slug = models.SlugField(max_length=100, unique_for_month='pub_date')
    pub_date = models.DateTimeField('date published', default=timezone.now)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:article', args=[self.pub_date.year,
            "{:02d}".format(self.pub_date.month), self.slug])
    
    def save(self, *args, **kwargs):
        html = markdown.markdown(self.source_text)
        self.text = html
        if self.slug == None or self.slug == "":
            self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

class Comment(models.Model):
    article = models.ForeignKey(Article)
    name = models.CharField(max_length=30)
    text = models.TextField()
    pub_date = models.DateTimeField('date published', default=timezone.now)
    
    def __str__(self):
        return '{} on "{}" at {}'.format(self.name,
            self.article.title, self.pub_date)
    
    def get_absolute_url(self):
        return self.article.get_absolute_url() + "#comment-" + str(self.pk)

class Upload(models.Model):
    # TODO: Change upload_to to a callable, as per
    # http://stackoverflow.com/questions/1190697/django-filefield-with-upload-to-determined-at-runtime
    media_file = models.FileField(upload_to="%Y/%m")

