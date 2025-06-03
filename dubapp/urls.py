from django.urls import path
from . import views
from .views import progress
urlpatterns = [
    path('', views.video_upload, name='video_upload'),
    path('download/', views.download_video, name='download_video'),
    path('progress/', progress, name='progress'),
]
