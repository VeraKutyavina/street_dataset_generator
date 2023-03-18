from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('create_video', views.create_video_view, name='test'),
    path('counting', views.counting_view, name='counting'),
    path('get_osm_data', views.get_osm_data, name='get_osm_data'),
    path('interface', views.user_form_view, name='user_form_view'),
]