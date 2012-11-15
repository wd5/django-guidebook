from django.conf.urls import patterns, include, url

# (?P<year>\d{4})
urlpatterns = patterns( 'guidebook',
    url( r'^add/$', 'views.add', name = 'guidebook-add' ),
    url( r'^edit/(?P<id>\d+)$', 'views.edit', name = 'guidebook-edit' ),
    url( r'^category-(?P<id>\d+)(?:\-(?P<slug>[\w\-]+))?(?:\/loc\-(?P<country>\d+))?(?:\:(?P<city>\d+))?(?:\/page-(?P<page>\d+))?', 'views.category', name = 'guidebook-category' ),
    url( r'^post-(?P<id>\d+)(?:\-(?P<slug>[\w\-]+))?', 'views.post', name = 'guidebook-post' ),
    url( r'^file/$', 'views.file', name = 'guidebook-file' ),
    url( r'^ajax/image-upload/$', 'ajax.image_upload', name = 'guidebook-ajax-image-upload' ),
    url( r'^(?:loc\-(?P<country>all|\d+))?(?:\:(?P<city>\d+))?(?:/?page-(?P<page>\d+))?', 'views.home', name = 'guidebook-home' ),
 )

