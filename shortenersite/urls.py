from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # NOTE admin goes before others to ensure its pattern is recognized first.
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('shortener.urls')),
]
