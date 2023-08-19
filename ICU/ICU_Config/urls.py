from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ICU_App', include('ICU_App.urls')),
]
