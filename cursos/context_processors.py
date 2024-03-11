from .models import Curso

def categorias_disponiveis(request):
    categorias = Curso.objects.values_list('categoria', flat=True).distinct()
    return {'categorias': categorias}