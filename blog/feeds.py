"""
Feeds for the blog app.
"""

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse

from .models import Article, Category

class LatestArticlesFeed(Feed):
    """
    A feed of the latest published articles on the blog, including the full
    article text.
    """
    title = "Inspiration Forge"
    description = "Ideas for Nerds!" # TODO: Make this come from settings?
    
    def author_name(self):
        return "Inspiration Forge"
    
    def link(self):
        return reverse("blog:rssfeed")
    
    def items(self):
        return Article.published_articles()
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.text
    
    def item_pubdate(self, item):
        return item.pub_date
    
    def item_author_name(self, item):
        return ", ".join(
            [str(contributor) for contributor in item.contributors.all()]
        )
    
    def item_enclosure_url(self, item):
        if item.enclosure_url.strip():
            return item.enclosure_url
        else:
            return None
        
    def item_enclosure_mime_type(self, item):
        if item.enclosure_mime_type.strip():
            return item.enclosure_mime_type
        else:
            return None
        
    def item_enclosure_length(self, item):
        return item.enclosure_length


class CategoryFeed(LatestArticlesFeed):
    """
    A feed for a specific category of article.
    """
    def title(self, obj):
        if obj.title:
            return obj.title
        else:
            return "Inspiration Forge: {}".format(obj.name)
    
    def link(self, obj):
        return reverse("blog:categoryfeed", args=[obj.slug])
    
    def description(self, obj):
        if obj.description:
            return obj.description
        else:
            return "Ideas for Nerds! ({})".format(obj.name)
    
    def items(self, obj):
        return super().items().filter(category=obj)
        
    def get_object(self, request, slug):
        return Category.objects.get(slug=slug)

