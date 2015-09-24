# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.text import slugify

def generate_slug(apps, schema_editor):
    Article = apps.get_model("blog", "Article")
    for article in Article.objects.all():
        if article.slug == "":
            article.slug = slugify(article.title)
            article.save()

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_article_slug'),
    ]

    operations = [
        migrations.RunPython(generate_slug)
    ]

