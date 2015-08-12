# Create your views here.
# coding=utf-8
from django.contrib.auth.hashers import make_password


from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required

from principal.models import Entry, Comentario, Mensaje
from principal.forms import EntradaForm, EditarContrasenaForm, EditarEmailForm, ComentarioForm, MensajeForm


"""Listar todas las entradas del blog"""
def lista_entrada(request):
	entradas = Entry.objects.all().order_by('created').reverse()
	paginator = Paginator(entradas, 2)

	try: page = int(request.GET.get("page", '1'))
	except ValueError: page = 1

	try:
		entradas = paginator.page(page)
	except (InvalidPage, EmptyPage):
		entradas = paginator.page(paginator.num_pages)
	return render_to_response('index.html',{'lista':entradas}, context_instance=RequestContext(request))


"""Nueva entrada del blog"""
@login_required(login_url='/ingresar')
def nuevaentrada(request):
		if request.method=='POST':
			formulario=EntradaForm(request.POST)
			if formulario.is_valid():
				entrada=formulario.save(commit=False)
				entrada.author=request.user
				entrada.publicado=True
				entrada.save()
				return HttpResponseRedirect('/')
		else:
			formulario=EntradaForm()
		return render_to_response('nueva_entrada.html', {'formulario':formulario}, context_instance=RequestContext(request))
	

"""Editar entrada del blog"""
@login_required(login_url='/ingresar')
def editar_entrada(request, id_entrada):
	usuario = request.user
	entrada = Entry.objects.get(pk=id_entrada)
	if usuario == entrada.author:
		if request.method == 'POST':
			formulario = EntradaForm(request.POST, instance=entrada)
			if formulario.is_valid():
				formulario.save()
				return HttpResponseRedirect('/misentradas')
		else:
			formulario = EntradaForm(instance=entrada)
		return render_to_response('nueva_entrada.html', {'formulario':formulario}, context_instance=RequestContext(request))
	else:
		return render_to_response('/ingresar', context_instance=RequestContext(request))


"""Ver entradas del usuario logueado"""
@login_required(login_url='/ingresar')
def milista_entrada(request):
	entradas = Entry.objects.filter(author=request.user).order_by('created').reverse()
	return render_to_response('usuario_mis_entradas.html',{'lista':entradas}, context_instance=RequestContext(request))


"""Eliminar entrada"""
@login_required(login_url='/ingresar')
def eliminar_entrada(request, id_entrada):
	entrada=Entry.objects.get(pk=id_entrada)
	usuario = request.user
	if usuario==entrada.author or usuario.is_superuser:
		entrada.delete()
		return HttpResponseRedirect('/misentradas')
	else:
		return render_to_response('/ingresar', context_instance=RequestContext(request))


"""Filtrar categoria de las entradas"""
def ver_categoria(request, nombre_categoria):
	entradas = Entry.objects.all().filter(categoria=nombre_categoria)
	paginator = Paginator(entradas, 2)

	try: page = int(request.GET.get("page", '1'))
	except ValueError: page = 1

	try:
		entradas = paginator.page(page)
	except (InvalidPage, EmptyPage):
		entradas = paginator.page(paginator.num_pages)

	return render_to_response('entrada.html',{'lista':entradas}, context_instance=RequestContext(request))


"""Registrar un nuevo usuario"""
def nuevo_usuario(request):
	if request.method=='POST':
		formulario = UserCreationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST['username']
			usuario2 = User.objects.filter(username=usuario)
			if usuario2:
				return render_to_response('usuario_repetido.html', context_instance=RequestContext(request))
			else:
				formulario.save()
				return HttpResponseRedirect('/ingresar')
	else:
		formulario = UserCreationForm()
	return render_to_response('usuario_registro.html', {'formulario':formulario}, context_instance=RequestContext(request))


"""Loguearse un usuario"""
def ingresar(request):
	if not request.user.is_anonymous():
		return HttpResponse('privado')
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/privado')
				else:
					return render_to_response('usuario_noactivo.html', context_instance=RequestContext(request))
			else:
				return render_to_response('usuario_login_error.html', context_instance=RequestContext(request))
	else:
		formulario = AuthenticationForm()
	return render_to_response('usuario_login.html', {'formulario':formulario}, context_instance=RequestContext(request))


"""Usuario no activo"""
@login_required(login_url='/ingresar')
def privado(request):
	usuario = request.user
	return render_to_response('privado.html', {'usuario':usuario} , context_instance=RequestContext(request))


"""Cerrar sesion"""
@login_required(login_url='/ingresar')
def cerrar(request):
	logout(request)
	return HttpResponseRedirect('/')


"""Ver todos los usuarios"""
@login_required(login_url='/ingresar')
def lista_usuarios(request):
	entradas = User.objects.all().exclude(username=request.user).order_by('username')
	return render_to_response('usuarios.html',{'lista':entradas}, context_instance=RequestContext(request))


"""Ver una sola entrada"""
def ver_entrada(request, id_entrada):
	entradas = Entry.objects.all().filter(id=id_entrada)
	comentarios = Comentario.objects.all().filter(entry=id_entrada)
	return render_to_response('entrada.html',{'lista':entradas, 'lista2':comentarios}, context_instance=RequestContext(request))


"""Ver un solo usuario"""
@login_required(login_url='/ingresar')
def ver_usuario(request, id_entrada):
	entradas = User.objects.all().filter(username=id_entrada)
	return render_to_response('usuarios.html',{'lista':entradas}, context_instance=RequestContext(request))


"""Panel de control del usuario"""
@login_required(login_url='/ingresar')
def panel_usuario(request):
	entradas = User.objects.all().filter(username=request.user)
	return render_to_response('usuario_panel_de_control.html',{'lista':entradas}, context_instance=RequestContext(request))


"""Editar contraseña del usuario"""
@login_required(login_url='/ingresar')
def editar_contrasena(request):
	if request.method=='POST':
		formulario = EditarContrasenaForm(request.POST)
		if formulario.is_valid:
			password = request.POST['password']
			password2 = request.POST['password2']
			if password != password2:
				return render_to_response('contrasenas_incorrectas.html', context_instance=RequestContext(request))
			else:
				request.user.set_password(password)
				request.user.save()
				return render_to_response('contraseña_cambiada.html', context_instance=RequestContext(request))
	else:
		formulario = EditarContrasenaForm()
	return render_to_response('editar_contrasena.html', {'formulario':formulario}, context_instance=RequestContext(request))


"""Editar email del usuario"""
@login_required(login_url='/ingresar')
def editar_email(request):
	if request.method=='POST':
		formulario = EditarEmailForm(request.POST)
		if formulario.is_valid:
			email = request.POST['email']
			request.user.email = email
			comprobar = User.objects.filter(email=email)
			if comprobar:
				return render_to_response('email_repetido.html', context_instance=RequestContext(request))
			else:
				request.user.save()
				return render_to_response('email_cambiado.html', context_instance=RequestContext(request))
	else:
			formulario = EditarEmailForm()
	return render_to_response('editar_email.html', {'formulario':formulario}, context_instance=RequestContext(request))


"""Nuevo comentario"""
@login_required(login_url='/ingresar')
def nuevocomentario(request, id_entrada):
		if request.method=='POST':
			formulario=ComentarioForm(request.POST)
			if formulario.is_valid():
				comentario=formulario.save(commit=False)
				comentario.user=request.user
				comentario.entry=Entry.objects.get(pk=id_entrada)
				comentario.save()
				entradas = Entry.objects.all().filter(id=id_entrada)
				comentarios = Comentario.objects.all().filter(entry=id_entrada)
				return render_to_response('entrada.html',{'lista':entradas, 'lista2':comentarios}, context_instance=RequestContext(request))		
		else:
			formulario=ComentarioForm()
		return render_to_response('nuevo_comentario.html', {'formulario':formulario}, context_instance=RequestContext(request))

"""Eliminar comentario"""
@login_required(login_url='/ingresar')
def eliminar_comentario(request, id_entrada, id_entrada2):
	comentario=Comentario.objects.get(pk=id_entrada)
	usuario = request.user
	if usuario==comentario.user or usuario.is_superuser:
		comentario.delete()
		entradas = Entry.objects.all().filter(id=id_entrada2)
		comentarios = Comentario.objects.all().filter(entry=id_entrada2)
		return render_to_response('index.html',{'lista':entradas, 'lista2':comentarios}, context_instance=RequestContext(request))

"""Editar comentario"""
@login_required(login_url='/ingresar')
def editar_comentario(request, id_entrada, id_entrada2):
	user = request.user
	comentario = Comentario.objects.get(pk=id_entrada)
	if user == comentario.user:
		if request.method == 'POST':
			formulario = ComentarioForm(request.POST, instance=comentario)
			if formulario.is_valid():
				formulario.save()
				entradas = Entry.objects.all().filter(id=id_entrada2)
				comentarios = Comentario.objects.all().filter(entry=id_entrada2)
				return render_to_response('index.html',{'lista':entradas, 'lista2':comentarios}, context_instance=RequestContext(request))
		else:
			formulario = ComentarioForm(instance=comentario)
		return render_to_response('nueva_entrada.html', {'formulario':formulario}, context_instance=RequestContext(request))
	else:
		return render_to_response('/ingresar', context_instance=RequestContext(request))

"""Mensajes privados"""
@login_required(login_url='/ingresar')
def nuevomensaje(request, usuario):
		if request.method=='POST':
			formulario=MensajeForm(request.POST)
			if formulario.is_valid():
				mensaje=formulario.save(commit=False)
				mensaje.user=request.user
				mensaje.addressee=usuario
				mensaje.save()
				return HttpResponseRedirect('/usuarios')
		else:
			formulario=MensajeForm()
		return render_to_response('nuevo_mensaje.html', {'formulario':formulario}, context_instance=RequestContext(request))

"""Bandeja de entrada mensajes privados"""
@login_required(login_url='/ingresar')
def bandeja_entrada(request):
	mensajes = Mensaje.objects.all().filter(addressee=request.user).order_by('created').reverse()
	return render_to_response('bandeja_entrada.html',{'lista':mensajes}, context_instance=RequestContext(request))

"""Bandeja de salida mensajes privados"""
@login_required(login_url='/ingresar')
def bandeja_salida(request):
	mensajes = Mensaje.objects.all().filter(user=request.user).order_by('created').reverse()
	return render_to_response('bandeja_salida.html',{'lista':mensajes}, context_instance=RequestContext(request))
