from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/save_screenshot', views.SaveScreenshot.as_view(), name='save-screenshot'),
    path('test', views.test, name='test'),
    path('create_frames', views.create_frames, name='create_frames'),
    path('webp_mp4', views.webp_mp4, name='webp_mp4'),
    path('counting', views.counting, name='counting')
]