from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

emails_blacklisted = [
	"@yopmail.com", 
	"@mygeoweb.info", 
	"@hideweb.xyz", 
	"@mailbox87.de", 
	"@mailbox52.ga", 
	"@mailbox92.biz",
	"@tryzoe.com",

]

class ContactForm(forms.Form):
	fullname = forms.CharField(
		widget=forms.TextInput(
			attrs={
			"class": "form-control", 
			"placeholder": "Nombre Completo"
			}
		))

	email = forms.EmailField(widget=forms.EmailInput(
			attrs={
			"class": "form-control", 
			"placeholder": "Correo Electrónico"
			}
		))

	content = forms.CharField(widget=forms.Textarea(
		attrs={
			"class": "form-control",
			"placeholder": "Mensaje"
		}))

	def clean_email(self, emails_blacklisted = emails_blacklisted):
		email = self.cleaned_data['email']
		for item in emails_blacklisted:
			if item in email:
				raise forms.ValidationError("El correo indicado no es válido.")
		return email

class LoginForm(forms.Form):
	username = forms.CharField(
		widget=forms.TextInput(
			attrs={
			"class": "form-control", 
			"placeholder": "Nombre de usuario o email"
			}
		))
	password = forms.CharField(
		widget=forms.PasswordInput(
			attrs={
			"class": "form-control", 
			"placeholder": "Contraseña"
			}
		))	

class RegisterForm(forms.Form):
	username = forms.CharField(
		widget=forms.TextInput(
			attrs={
			"class": "form-control", 
			"placeholder": "Correo Electrónico"
			}
		))

	email = forms.EmailField(widget=forms.EmailInput(
			attrs={
			"class": "form-control", 
			"placeholder": "Correo Electrónico"
			}
		))

	password = forms.CharField(
		widget=forms.PasswordInput(
			attrs={
			"class": "form-control", 
			"placeholder": "Contraseña"
			}
		))

	password2 = forms.CharField(
		widget=forms.PasswordInput(
			attrs={
			"class": "form-control", 
			"placeholder": "Repetir Contraseña"
			}
		))

	def clean_username(self):
		username = self.cleaned_data.get('username')
		qs = User.objects.filter(username=username)
		if qs.exists():
			raise forms.ValidationError("El nombre de usuario ya esta registrado en el sistema")
		return username	

	def clean_email(self):
		email = self.cleaned_data.get('email')
		qs = User.objects.filter(email=email)
		if qs.exists():
			raise forms.ValidationError("El correo ya se encuentra registrado en el sistema")	
		for item in emails_blacklisted:
			if item in self.cleaned_data.get('email'):
				raise forms.ValidationError("El correo indicado no es válido.")
		return email			

	def clean_passwords(self):
		data = self.cleaned_data
		password = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password != password2:
			raise forms.ValidationError("Las contraseñas deben coincidir")
		return data	

	# address_1 = forms.CharField(
	# 	widget=forms.TextInput(
	# 		attrs={
	# 		"class": "form-control", 
	# 		"placeholder": "Direción (Avenida, Calle, Urbanización)"
	# 		}
	# 	))

	# address_2 = forms.CharField(
	# 	widget=forms.TextInput(
	# 		attrs={
	# 		"class": "form-control", 
	# 		"placeholder": "Continuacion de la direción (opcional)"
	# 		}
	# 	))

	# reference = forms.CharField(
	# 	widget=forms.TextInput(
	# 		attrs={
	# 		"class": "form-control", 
	# 		"placeholder": "Punto de Referencia"
	# 		}
	# 	))

	# zip_code = forms.CharField(
	# 	widget=forms.TextInput(
	# 		attrs={
	# 		"class": "forms.form-control", ()
 	# 		"placeholder": "Código Postal"Las contraseñas deben coincidir""
# else:
# 	return email	
	# 		}
	# 	))

	# STATES_CHOICES = ('Distrito Capital', 'MIRANDA')

	# state = forms.ChoiceField(choices=STATES_CHOICES)