from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Curso, Profile, Inscricao
from .forms import CursoForm
from django.contrib.auth import login, logout
from .forms import UserRegisterForm



#Index

def index(request):
    # Aqui você pode adicionar lógica para passar contexto, se necessário
    return render(request, 'index.html')

#Usuário

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user immediately after registering
            # Redirecionar para a página inicial após o registro
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def logout_request(request):
    logout(request)
    return redirect('index')


@login_required
def perfil_usuario(request):
    cursos_criados = Curso.objects.filter(criador=request.user)
    inscricoes = Inscricao.objects.filter(usuario=request.user).select_related('curso')
    return render(request, 'perfil_usuario.html', {
        'cursos_criados': cursos_criados,
        'inscricoes': inscricoes,
    })

#Cursos


def lista_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'lista_cursos.html', {'cursos': cursos})

def detalhes_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    return render(request, 'detalhes_curso.html', {'curso': curso})


def categoria_cursos(request, categoria):
    cursos = Curso.objects.filter(categoria=categoria)
    return render(request, 'categoria_cursos.html', {'cursos': cursos, 'categoria': categoria})


def buscar_curso(request):
    query = request.GET.get('q')
    resultados = Curso.objects.filter(titulo__icontains=query)
    return render(request, 'resultados_busca.html', {'cursos': resultados})


@login_required
def comprar_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    usuario = request.user
    perfil = usuario.profile
    
    if perfil.creditos > 0:
        perfil.creditos -= 1  # Subtrai crédito do comprador
        perfil.save()
        
        criador_perfil = curso.criador.profile
        criador_perfil.creditos += 1  # Adiciona crédito ao criador
        criador_perfil.save()
        
        curso.inscricoes += 1
        curso.save()
        
        # Redireciona para a página de sucesso ou detalhes do curso
        return redirect('caminho_para_sucesso_ou_curso', curso_id=curso_id)
    else:
        # Redireciona para uma página de erro ou informação
        return redirect('caminho_para_erro_ou_informacao')


@login_required
def like_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    curso.likes += 1
    curso.save()
    
    criador_perfil = curso.criador.profile
    criador_perfil.creditos += 1  # Adiciona crédito ao criador por like
    criador_perfil.save()
    
    return redirect('algum_caminho_após_like', curso_id=curso_id)

@login_required
def dislike_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    curso.dislikes += 1
    curso.save()
    
    criador_perfil = curso.criador.profile
    criador_perfil.creditos -= 1  # Remove crédito do criador por dislike, com lógica adicional para evitar créditos negativos
    criador_perfil.save()
    
    return redirect('algum_caminho_após_dislike', curso_id=curso_id)




@login_required
def criar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            novo_curso = form.save(commit=False)
            novo_curso.criador = request.user
            novo_curso.save()
            # Redireciona para a página de detalhes do curso após a criação
            return redirect('detalhes_curso', curso_id=novo_curso.id)
    else:
        form = CursoForm()
    return render(request, 'criar_curso.html', {'form': form})