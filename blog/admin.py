from django.contrib import admin

from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'title', 'source_text']
    list_display = ('title', 'pub_date')
    list_filter = ['pub_date']
    
    class Media:
        css = {
            "all": ("css/admin/article-admin.css",)
        }

admin.site.register(Article, ArticleAdmin)

