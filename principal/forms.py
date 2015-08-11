from django.forms import ModelForm
from django_markdown.widgets import MarkdownWidget
from django import forms
from principal.models import Entry, Comentario, Mensaje
# coding=utf-8

class EntradaForm(ModelForm):
	body = forms.CharField(widget=MarkdownWidget())
	class Meta:
		model = Entry

		fields = ('title', 'body')

class EditarContrasenaForm(forms.Form):
    password = forms.CharField(
        label='Nueva contrasena',
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(
        label='Repetir contrasena',
        min_length=5,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class EditarEmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}))


class ComentarioForm(ModelForm):
    body = forms.CharField(widget=MarkdownWidget())
    class Meta:
        model = Comentario

        fields = ('title', 'body')

class MensajeForm(ModelForm):
    body = forms.CharField(widget=MarkdownWidget())
    class Meta:
        model = Mensaje

        fields = ('title', 'body')