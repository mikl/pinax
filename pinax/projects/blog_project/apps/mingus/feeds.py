from django.utils.feedgenerator import Atom1Feed
from django.contrib.sites.models import Site
from django.contrib.syndication.feeds import Feed

from threadedcomments.models import ThreadedComment

class LatestComments(Feed):
    title = "%s: latest comments" % Site.objects.get_current().name
    link = "/feeds/comments/"
    subtitle = "The latest 25 comments posted on the blog."
    feed_type = Atom1Feed

    def items(self):
        return ThreadedComment.objects.order_by('-submit_date')[:25]

    def item_link(self, item):
        return "%s#comment-%d" % (item.content_object.get_absolute_url(), item.id)

    def item_author_name(self, item):
        return item.name

    def item_author_link(self, item):
        return item.website

    def item_pubdate(self, item):
        return item.date_submitted

