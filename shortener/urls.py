from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home_page, name='home_page'),
    url(r'^preview/(?P<token>.*)$', views.preview, name='preview'),
    url(r'^(?P<token>.*)$', views.token_redirect, name='token_redirect'),
]
