from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


def return_empty(request):
    return HttpResponse('')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ICU_App/', include('ICU_App.urls')),
    path('favicon.ico', return_empty),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)