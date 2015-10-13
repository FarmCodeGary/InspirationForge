# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import blog.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='media_file',
            field=models.ImageField(upload_to=blog.models.image_filename),
        ),
    ]
