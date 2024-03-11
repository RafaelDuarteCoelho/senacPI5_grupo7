from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Curso(models.Model):
    NIVEL_CHOICES = [
        ('IN', 'Iniciante'),
        ('IT', 'Intermediário'),
        ('AV', 'Avançado'),
    ]
    
    titulo = models.CharField(max_length=255)
    descricao = models.TextField()
    criador = models.ForeignKey(User, on_delete=models.CASCADE)
    inscricoes = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    duracao = models.DurationField()
    categoria = models.CharField(max_length=100)
    nivel = models.CharField(max_length=2, choices=NIVEL_CHOICES)
    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to='cursos_thumbnails/', null=True, blank=True)
    preco_creditos = models.PositiveIntegerField(default=1)
    descricao_breve = models.CharField(max_length=255, blank=True)
    idioma = models.CharField(max_length=50)
    status = models.CharField(max_length=100, default='Ativo')


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creditos = models.IntegerField(default=3)

    def __str__(self):
        return f'Perfil de {self.user.username}'
    

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()


class Inscricao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscricoes')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscritos')
    data_inscricao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['usuario', 'curso']
