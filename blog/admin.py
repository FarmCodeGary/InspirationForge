from django.contrib import admin

from .models import Article, Comment

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class ArticleAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'title', 'slug', 'source_text']
    list_display = ('title', 'pub_date')
    list_filter = ['pub_date']
    inlines = [CommentInline]
    
    class Media:
        css = {
            "all": ("css/admin/article-admin.css",)
        }

class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'name', 'text', 'pub_date')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)

