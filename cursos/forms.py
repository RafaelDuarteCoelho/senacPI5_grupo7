from django import forms
from .models import Curso
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['titulo', 'descricao', 'duracao', 'categoria', 'nivel', 'thumbnail', 'descricao_breve', 'idioma']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']