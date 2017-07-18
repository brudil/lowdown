from lowdown.manage.content import views
from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<pk>\w+)/metadata/$', views.RetrieveEditorialMetadata.as_view()),
    url(r'^(?P<pk>\w+)/revision/$', views.CreateRevision.as_view()),
    url(r'^revisions/(?P<pk>\w+)/publish/$', views.PublishContentRevision.as_view()),
    url(r'^revisions/(?P<pk>\w+)/status/$', views.StatusContentRevision.as_view()),
    url(r'^(?P<pk>\w+)/revision/current/$', views.RetrieveCurrentRevision.as_view()),
]
