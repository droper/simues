from django.conf.urls import url

from . import views

import resumenact


urlpatterns = [
    url(r'^$', resumenact.views.index, name='index'),
    url(r'^(?P<actividad_id>[0-9]+)/$', views.lista, name='lista'),
    url(r'^registro/(?P<actividad_id>[0-9]+)/$', views.registro_cadena, name='registro'),
    url(r'^editar/(?P<cadena_id>[0-9]+)/$', views.editar, name='editar'),
    url(r'^registro_punto_muestreo/(?P<cadena_id>[0-9]+)/$', views.registro_punto_muestreo,
        name='registro_punto_muestreo'),
    url(r'^editar_punto_muestreo/(?P<punto_id>[0-9]+)/$', views.editar_punto_muestreo,
        name='editar_punto_muestreo'),
    url(r'^subir_xml_punto_muestreo/(?P<punto_id>[0-9]+)/$', views.subir_xml_punto_muestreo,
        name='subir_xml_punto_muestreo'),
]