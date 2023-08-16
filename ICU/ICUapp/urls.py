from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.main, name='live_stream'),
    path('notify/', views.notify, name='notify'),
]
