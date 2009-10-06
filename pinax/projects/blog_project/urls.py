from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
from django.conf import settings
from basic.blog import views as blog_views
from basic.blog.feeds import BlogPostsFeed, BlogPostsByCategory
from basic.blog.sitemap import BlogSitemap
from mingus.feeds import LatestComments
from mingus.views import springsteen_results, springsteen_firehose, \
                            home_list, springsteen_category, contact_form

admin.autodiscover()

feeds = {
    'latest': BlogPostsFeed,
    'categories': BlogPostsByCategory,
    'comments': LatestComments,
}
#ex: /feeds/latest/
#ex: /feeds/categories/django/

sitemaps = {
    'posts': BlogSitemap,
}

# override the default handler500 so we pass MEDIA_URL (nod to oebfare)
handler500 = "mingus.views.server_error"

urlpatterns = patterns('',
    url(r'^admin/password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    (r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete'),
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^$', view=home_list, name='home_index'),
    (r'^blog/', include('basic.blog.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^profiles/', include('basic_profiles.urls')),
    (r'^avatar/', include('avatar.urls')),
    url(r'^page/(?P<page>\w)/$', view=home_list, name='home_paginated'),
    url(r'^oops/$', 'mingus.views.oops', name='raise_exception'),
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^api/springsteen/posts/$', springsteen_results),
    (r'^api/springsteen/firehose/$', springsteen_firehose),
    (r'^api/springsteen/category/(?P<slug>[-\w]+)/$', springsteen_category),

    url(r'^contact/$', contact_form, name='contact_form'),
    url(r'^contact/sent/$',
        direct_to_template,
        { 'template': 'contact_form/contact_form_sent.html' },
        name='contact_form_sent'),

)


if settings.LOCAL_DEV:
    urlpatterns += patterns('django.views.static',
        (r'^%s(?P<path>.*)' % settings.STATIC_URL[1:], 'serve',
         {'document_root': settings.STATIC_ROOT}),
        (r'^%s(?P<path>.*)' % settings.MEDIA_URL[1:], 'serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

