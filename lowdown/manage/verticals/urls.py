from lowdown.manage.verticals import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.ListVerticals.as_view()),
]
