from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.main, name='live_stream'),
    path('live_feed/', views.live_feed, name='live_feed'),
    path('notify/', views.notify, name='notify'),
    path('analyze/', views.analyze, name='analyze'),
]
