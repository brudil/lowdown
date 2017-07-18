from .views import ListCreateTopic, RetrieveUpdateDestroyTopic
from django.conf.urls import url

urlpatterns = [
    url(r'^$', ListCreateTopic.as_view()),
    url(r'^(?P<pk>\w+)/$', RetrieveUpdateDestroyTopic.as_view()),
]
