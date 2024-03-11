
from django.contrib import admin
from django.urls import include, path
from cursos import views as curso_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cursos.urls')),
    path('', curso_views.index, name='index'),
]