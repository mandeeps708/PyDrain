##
# @package civilsage.urls
# This module contain urlspatterns to map to html file in django.
#...
# @author amarjeet kapoor

from django.conf.urls import url

from . import views

urlpatterns = [
	#directs to index veiw
    url(r'^$', views.index, name='index'),
    url(r'^file/$',views.file,name='file'),
]



