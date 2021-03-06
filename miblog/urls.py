from django.conf.urls import patterns, include, url
from django.contrib import admin



urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','principal.views.lista_entrada'),
    url(r'^usuarionuevo$','principal.views.nuevo_usuario'),
    url(r'^ingresar/$','principal.views.ingresar'),
    url(r'^privado/$','principal.views.privado'),
    url(r'^cerrar/$', 'principal.views.cerrar'),
    url(r'^entrada/$', 'principal.views.nuevaentrada'),
    url(r'^misentradas/$','principal.views.milista_entrada'),
    url('^markdown/', include( 'django_markdown.urls')),
    url(r'^eliminar/(?P<id_entrada>\S+)$', 'principal.views.eliminar_entrada'),
    url(r'^editar/(?P<id_entrada>\S+)$', 'principal.views.editar_entrada'),
    url(r'^usuarios/$', 'principal.views.lista_usuarios'),
    url(r'^verentrada/(?P<id_entrada>\S+)$', 'principal.views.ver_entrada'),
    url(r'^verusuario/(?P<id_entrada>\S+)$', 'principal.views.ver_usuario'),
    url(r'^panelusuario/$', 'principal.views.panel_usuario'),
    url(r'^editar_contrasena/$', 'principal.views.editar_contrasena'),
    url(r'^editar_email/$', 'principal.views.editar_email'),
    url(r'^comentario/(?P<id_entrada>\S+)$', 'principal.views.nuevocomentario'),
    url(r'^eliminarcomentario/(?P<id_entrada>\S+)/(?P<id_entrada2>\S+)$', 'principal.views.eliminar_comentario'),
    url(r'^editarcomentario/(?P<id_entrada>\S+)/(?P<id_entrada2>\S+)$', 'principal.views.editar_comentario'),
    url(r'^nuevo_mensaje/(?P<usuario>\S+)$', 'principal.views.nuevomensaje'),
    url(r'^bandeja_entrada/$', 'principal.views.bandeja_entrada'),
    url(r'^bandeja_salida/$', 'principal.views.bandeja_salida'),
    url(r'^categoria/(?P<nombre_categoria>\S+)$', 'principal.views.ver_categoria'),
)
