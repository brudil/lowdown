from django.conf.urls import url
from .views import stub_count

urlpatterns = [
    url(r'^unread/count', stub_count)
]
