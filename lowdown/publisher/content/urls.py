from lowdown.publisher.content import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.ListContent.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', views.RetrieveContent.as_view()),
]
