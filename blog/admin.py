from django.contrib import admin

from .models import Article, Comment, Tag

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'title', 'slug', 'tags', 'source_text']
    list_display = ('title', 'pub_date')
    list_filter = ['pub_date']
    inlines = [CommentInline]
    
    class Media:
        css = {
            "all": ("css/admin/article-admin.css",)
        }

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('article', 'name', 'text', 'pub_date')
    list_display_links = ('text',)

admin.site.register(Tag)

