from lowdown.manage.authors import views
from django.conf.urls import url

urlpatterns = [
    url(r'', views.ListAuthors.as_view()),
]
