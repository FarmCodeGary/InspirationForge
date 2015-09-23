from django.db import models
from django.utils import timezone

import markdown

class Article(models.Model):
    title = models.CharField(max_length=50)
    source_text = models.TextField()
    text = models.TextField(editable=False)
    pub_date = models.DateTimeField('date published',default=timezone.now)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        html = markdown.markdown(self.source_text)
        self.text = html
        super(Article, self).save(*args, **kwargs)

