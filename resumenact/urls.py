from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^registro/$', views.index, name='index'),
    url(r'^registro/(?P<actividad_id>[0-9]+)/$', views.registro, name='registro'),
    url(r'^elegir_cargo_inspectores/(?P<actividad_id>[0-9]+)/$', views.elegir_cargo_inspectores,
        name='elegir_cargo_inspectores'),

    # Ajax urls
    url(r'^obtener_unidades/(?P<administrado_id>[\w-]+)/$', views.obtener_unidades, name='obtener_unidades'),
    url(r'^obtener_subtipos_supervision/(?P<tiposupervision_id>[\w-]+)/$',
        views.obtener_subtipos_supervision, name='obtener_subtipos_supervision')


]