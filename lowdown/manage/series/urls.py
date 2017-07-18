from .views import RetrieveUpdateDestroyTopic
from django.conf.urls import url

urlpatterns = [
    url(r'(?P<cpk>\w+)/$', RetrieveUpdateDestroyTopic.as_view()),
]
