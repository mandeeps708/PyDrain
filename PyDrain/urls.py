##
# @package sage.urls
# This module contain urlspatterns to map to  civilsage.urls in django.
#...
# @author amarjeet kapoor

from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    url(r'^',include('pydrain.urls',namespace='pydrain')),
    #url for admin login
    url(r'^admin/', include(admin.site.urls)),
)
