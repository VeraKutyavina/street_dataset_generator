from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/save_screenshot', views.SaveScreenshot.as_view(), name='save-screenshot'),
    path('test', views.test, name='test')
]