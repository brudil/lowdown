"""lowdown URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from rest_framework_jwt.views import obtain_jwt_token
from graphene_django.views import GraphQLView

# manage
from lowdown.manage.content import urls as manage_content_urls
from lowdown.manage.content.views import ListCreateContent
from lowdown.manage.users import urls as manage_users_urls
from lowdown.manage.notifications import urls as manage_notifications_urls
from lowdown.manage.topics import urls as manage_topics_urls
from lowdown.manage.sections import urls as manage_sections_urls
from lowdown.manage.sections.views import ListCreateSection
from lowdown.manage.multimedia.views import ListCreateMultimedia
from lowdown.manage.multimedia import urls as manage_multimedia_urls
from lowdown.manage.authors import urls as manage_authors_urls
from lowdown.manage.verticals import urls as manage_verticals_urls
from lowdown.manage.interactives import urls as manage_interactives_urls

# publisher
from lowdown.publisher.content import urls as publisher_content_urls

inner_verticals = [
    url(r'^content/$', ListCreateContent.as_view()),
    url(r'^media/$', ListCreateMultimedia.as_view()),
    url(r'^sections/$', ListCreateSection.as_view()),
    url(r'^topics/', include(manage_topics_urls)),
    url(r'^authors/', include(manage_authors_urls)),
]

manage_patterns = [
    url(r'^auth/login/', obtain_jwt_token),
    url(r'^users/', include(manage_users_urls)),
    url(r'^notifications/', include(manage_notifications_urls)),
    url(r'^sections/', include(manage_sections_urls)),
    url(r'^topics/', include(manage_topics_urls)),
    url(r'^media/', include(manage_multimedia_urls)),
    url(r'^interactives/', include(manage_interactives_urls)),
    url(r'^content/', include(manage_content_urls)),
    url(r'^verticals/', include(manage_verticals_urls)),
    url(r'^verticals/(?P<vertical>\w+)/', include(inner_verticals)),
]

publisher_patterns = [
    url(r'^content/', include(publisher_content_urls)),
]

urlpatterns = [
    url(r'^dj-admin/', admin.site.urls),
    url(r'^manage/', include(manage_patterns)),
    url(r'^@(?P<vertical>\w+)/', include(publisher_patterns)),
    url(r'^graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
