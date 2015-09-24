from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.core.urlresolvers import reverse

import markdown

class Article(models.Model):
    title = models.CharField(max_length=50)
    source_text = models.TextField()
    text = models.TextField(editable=False)
    slug = models.SlugField(unique_for_month='pub_date')
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

