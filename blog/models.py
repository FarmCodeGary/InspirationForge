from django.db import models
from django.utils import timezone

class Article(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    pub_date = models.DateTimeField('date published',default=timezone.now)
