from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'simues.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', include('resumenact.urls'), name="index"),
    url(r'^seguimiento/', include('resumenact.urls', namespace="resumenact")),
    url(r'^cadenas/', include('cadenas.urls', namespace="cadenas")),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('allauth.urls')),
]
