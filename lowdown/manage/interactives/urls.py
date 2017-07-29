from django.conf.urls import url
from .views import RetrieveUpdateDestroyInteractives, ListCreateInteractives, ListCreateInteractiveReleases, UpdateInteractiveRelease

urlpatterns = [
    url(r'^$', ListCreateInteractives.as_view()),
    url(r'^(?P<slug>[\w-]+)/$', RetrieveUpdateDestroyInteractives.as_view()),
    url(r'^(?P<slug>[\w-]+)/releases/$', ListCreateInteractiveReleases.as_view()),
    url(r'^(?P<slug>[\w-]+)/releases/(?P<rid>[\w-]+)/$', UpdateInteractiveRelease.as_view()),
]
