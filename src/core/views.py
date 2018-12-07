from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, get_user_model
from .forms import ContactForm, LoginForm, RegisterForm
from cart.models import Cart

def home_page(request):
	context = {	
	"title": "Página Principal"
	}
	return render(request, 'home.html', context)

def about_page(request):
	context = {
	"title": "Acerca de Nosotros"
	}
	return render(request, 'home.html', context )

User = get_user_model()
def register_page(request):
	if request.user.is_authenticated:	
		return redirect(home_page)
	form = RegisterForm(request.POST or None)
	context = {
	"form": form,
	}
	if form.is_valid():
		username = form.cleaned_data.get('username')
		email = form.cleaned_data.get('email')
		password = form.cleaned_data.get('password')
		User.objects.create_user(username, email, password)
	return render(request, 'auth/register.html', context)


def login_page(request):
	if request.user.is_authenticated:
		return redirect(home_page)
	form = LoginForm(request.POST or None)
	context = {
	"form": form,
	"title": "Iniciar Sesión"
	}
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(request, username = username, password = password)
		if user is not None:
			login(request, user)
			context['form'] = LoginForm()
			return redirect(home_page)
		else:
			print('errorrrrr')
	return render(request, 'auth/login.html', context)

def contact_page(request):
	form = ContactForm(request.POST or None)
	context = {
	"form" : form,
	"title": "Formulario de Contacto"
	}
	if form.is_valid():
		print(form.cleaned_data)

	return render(request, 'contact/contact.html', context)