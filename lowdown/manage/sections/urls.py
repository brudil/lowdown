from .views import RetrieveUpdateDestroySection, ListCreateSection, ListTopicsForSection
from django.conf.urls import url

urlpatterns = [
    url(r'^$', ListCreateSection.as_view()),
    url(r'^(?P<pk>\w+)/$', RetrieveUpdateDestroySection.as_view()),
    url(r'^(?P<pk>\w+)/topics/$', ListTopicsForSection.as_view()),
]
