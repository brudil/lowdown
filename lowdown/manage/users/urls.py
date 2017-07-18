from lowdown.manage.users import views
from django.conf.urls import url

urlpatterns = [
    url(r'me', views.detail_current_user),
    url(r'', views.ListUsers.as_view()),
]
