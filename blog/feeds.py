"""
Feeds for the blog app.
"""

from django.contrib.syndication.views import Feed

from .models import Article

class LatestArticlesFeed(Feed):
    """
    A feed of the latest published articles on the blog, including the full
    article text.
    """
    title = "Inspiration Forge"
    link = "/feed/"
    description = "Ideas for Nerds!" # TODO: Make this come from settings?
    
    def items(self):
        return Article.published_articles()
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.text

