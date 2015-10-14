from django.contrib.syndication.views import Feed

from .models import Article

class LatestArticlesFeed(Feed):
    title = "Inspiration Forge"
    link = "/feed/"
    description = "Ideas for Nerds!"
    
    def items(self):
        return Article.objects.order_by('-pub_date')
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.text

