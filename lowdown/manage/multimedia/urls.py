from .views import RetrieveUpdateDestroyMultimedia, ListCreateMultimedia
from django.conf.urls import url

urlpatterns = [
    url(r'^(?P<pk>\w+)/$', RetrieveUpdateDestroyMultimedia.as_view()),
    url(r'^$', ListCreateMultimedia.as_view()),
]
