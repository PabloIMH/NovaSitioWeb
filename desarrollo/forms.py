from django import forms
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
import re
from .models import Archivo, ArchivoItem

# Formulario personalizado para añadir usuarios
class CustomUserCreationForm(DjangoUserCreationForm):
    ROL_CHOICES = [
        ('superadmin', 'Administrador (Superusuario)'),
        ('cliente', 'Cliente (Suscriptor)')
    ]

    password_ingreso = forms.CharField(
        label="Contraseña de ingreso",
        widget=forms.TextInput,
        required=False,
        help_text="Deja este campo vacío para que se genere una contraseña automática y se envíe por correo."
    )
    
    rol = forms.ChoiceField(
        choices=ROL_CHOICES,
        label="Rol",
        help_text="Selecciona el rol del usuario: Administrador o Cliente (Suscriptor)."
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'password_ingreso', 'rol')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.instance.pk:  # Si es un nuevo usuario
            random_password = get_random_string(length=12)
            self.fields['password_ingreso'].initial = random_password
            self.fields['password1'].initial = random_password
            self.fields['password2'].initial = random_password
            
            # Añadir ayuda para contraseñas autogeneradas
            self.fields['password1'].help_text = "La contraseña será autogenerada si dejas este campo vacío."
            self.fields['password2'].help_text = "La confirmación de la contraseña será autogenerada si dejas este campo vacío."
            
            # Deshabilitar campos para evitar que se cambien
            self.fields['password1'].disabled = True
            self.fields['password2'].disabled = True

    # Validación del nombre de usuario
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^\w+$', username):
            raise ValidationError("El nombre de usuario solo puede contener letras, números y guiones bajos.")
        return username

    # Validación del formato del correo electrónico
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            raise ValidationError("El formato del correo electrónico no es válido.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        raw_password = self.cleaned_data.get('password_ingreso') or get_random_string(length=12)
        user.set_password(raw_password)

        # Asignar el rol según la selección
        rol = self.cleaned_data.get('rol')
        if rol == 'superadmin':
            user.is_staff = True  # El usuario será administrador
            user.is_superuser = True  # El usuario será superusuario
        else:
            user.is_staff = False  # Cliente no tiene acceso a la administración
            user.is_superuser = False  # Cliente no es superusuario
        
        if commit:
            user.save()
        return user
# Formulario de carga de archivos
class ArchivoForm(forms.ModelForm):
    class Meta:
        model = Archivo
        fields = ['titulo', 'descripcion', 'usuario_asignado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo usuarios que no son superusuarios
        self.fields['usuario_asignado'].queryset = User.objects.filter(is_superuser=False)

    def save(self, commit=True):
        instance = super().save(commit=False)  # Crear la instancia principal del modelo Archivo
        if commit:
            instance.save()  # Guardar el modelo Archivo
        return instance
