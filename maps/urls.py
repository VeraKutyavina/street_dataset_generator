from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_video', views.create_video, name='test'),
    path('counting', views.counting, name='counting'),
    path('get_osm_data', views.get_osm_data, name='get_osm_data'),
]