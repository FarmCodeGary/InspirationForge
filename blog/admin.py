from django.contrib import admin

from .models import Article, Comment, Tag, Image, Category, Contributor

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'pub_date', 'tags'),
        }),
        ('RSS enclosure', {
            'classes': ('collapse',),
            'fields': ('enclosure_url', 'enclosure_length',
                'enclosure_mime_type'),
        }),
        ('Content', {
            'fields': ('source_text',),
        }),
    )
    
    list_display = ('title', 'category', 'pub_date')
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
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Contributor)

