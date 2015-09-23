from django.contrib import admin

from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'title', 'text']
    list_display = ('title', 'pub_date')
    list_filter = ['pub_date']

admin.site.register(Article, ArticleAdmin)
