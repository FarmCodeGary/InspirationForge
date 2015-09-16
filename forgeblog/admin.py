from django.contrib import admin

from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'title', 'text']

admin.site.register(Article, ArticleAdmin)
