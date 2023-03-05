from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_video', views.create_video, name='test'),
    # path('create_frames', views.create_frames, name='create_frames'),
    path('webp_mp4', views.webp_mp4, name='webp_mp4'),
    path('counting', views.counting, name='counting')
]