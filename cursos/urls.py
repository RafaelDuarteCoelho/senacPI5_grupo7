from django.urls import path
from .views import lista_cursos, criar_curso, detalhes_curso, comprar_curso, like_curso, dislike_curso, index, logout_request, perfil_usuario, buscar_curso
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('lista_cursos', lista_cursos, name='lista_cursos'),
    path('curso/criar/', criar_curso, name='criar_curso'),
    path('curso/<int:curso_id>/', detalhes_curso, name='detalhes_curso'),
    path('curso/comprar/<int:curso_id>/', comprar_curso, name='comprar_curso'),
    path('curso/like/<int:curso_id>/', like_curso, name='like_curso'),
    path('curso/dislike/<int:curso_id>/', dislike_curso, name='dislike_curso'),
    path('logout/', logout_request, name='logout'),
    path('accounts/profile/', perfil_usuario, name='perfil_usuario'),
    path('categorias/<categoria>/', views.categoria_cursos, name='categoria_cursos'),
    path('buscar/', buscar_curso, name='buscar_curso'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)