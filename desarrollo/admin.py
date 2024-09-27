import os  # Import para gestionar la ruta de la imagen
from django.conf import settings
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.html import mark_safe
from .forms import CustomUserCreationForm
from .models import PerfilUsuario

# Formulario personalizado para la edición de usuarios que ignora cambios en la contraseña
class CustomUserChangeForm(forms.ModelForm):
    password = forms.CharField(label="Contraseña", required=False, widget=forms.HiddenInput)  # Ocultar el campo de contraseña

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_password(self):
        # Si el campo de contraseña está vacío, ignoramos la validación
        return self.cleaned_data['password'] or self.instance.password

# Inline para mostrar el perfil de usuario en la edición
class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil de Usuario'
    fields = ('imagen_perfil', 'rol')  # Asegúrate de que se muestran los campos correctos

class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    inlines = (PerfilUsuarioInline,)  # Añadir el inline para editar la imagen de perfil
    list_display = ('get_image_and_username', 'email', 'first_name', 'last_name', 'get_rol')  # Mostrar imagen junto con nombre de usuario
    list_filter = ('perfilusuario__rol',)  # Filtro basado en el rol de usuario
    search_fields = ('username', 'email')

    fieldsets = (
        (None, {'fields': ('username', 'email')}),  # Eliminamos el campo de contraseña
        ('Información personal', {'fields': ('first_name', 'last_name')}),  # Información del usuario
        ('Permisos', {'fields': ('is_staff', 'is_superuser')}),  # Campos de permisos
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'rol'),  
        }),
    )

    def get_rol(self, obj):
        return 'Administrador' if obj.is_superuser else 'Suscriptor'
    get_rol.short_description = 'Rol'  # Nombre de la columna "Rol"

    def get_image_and_username(self, obj):
        # img perfil
        if obj.perfilusuario and obj.perfilusuario.imagen_perfil:
            return mark_safe(f'<img src="{obj.perfilusuario.imagen_perfil.url}" width="40" height="40" style="border-radius: 30%; vertical-align: middle; margin-right: 10px;" /> {obj.username}')
        return obj.username
    get_image_and_username.short_description = 'Nombre de usuario'

    def enviar_correo_bienvenida(self, usuario, contraseña):
        subject = 'Tu cuenta en Nova Analytics ha sido creada'
        # Renderizar la plantilla 
        html_message = render_to_string('email_bienvenida.html', {
            'usuario': usuario,
            'contraseña': contraseña,
            'url_login': 'http://127.0.0.1:8000/login/',  # URL local para pruebas
        })
        
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        
        # Crear el objeto de correo electrónico
        email = EmailMessage(subject, html_message, from_email, [usuario.email])
        
        # Enviar el correo como HTML, sin adjuntar el logo
        email.content_subtype = 'html'  # Enviar el correo como HTML
        email.send(fail_silently=False)

    def save_model(self, request, obj, form, change):
        if not change:  # Si es un usuario nuevo
            random_password = form.cleaned_data['password1']
            obj.set_password(random_password)  # Asignar la contraseña generada
            
            # Asignar el rol
            rol = form.cleaned_data.get('rol')
            if rol == 'superadmin':  
                obj.is_staff = True  # Administrador
                obj.is_superuser = True  # Administrador tendrá acceso total como superusuario
            else:
                obj.is_staff = False  # Cliente (suscriptor)
                obj.is_superuser = False  # No es superusuario
            
            # Guardar el usuario antes de enviar el correo
            obj.save()
            
            # Enviar el correo con la contraseña generada
            self.enviar_correo_bienvenida(obj, random_password)
        else:
            # Solo establece la contraseña si se cambia
            if form.cleaned_data['password']:
                obj.set_password(form.cleaned_data['password'])
            super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        # Crear o actualizar el perfil de usuario si ya existe
        perfil, created = PerfilUsuario.objects.get_or_create(user=form.instance)

        # Sincronizar los permisos del usuario en función del rol seleccionado en el perfil
        if perfil.rol == 'admin':
            form.instance.is_staff = True
            form.instance.is_superuser = True
        else:
            form.instance.is_staff = False
            form.instance.is_superuser = False

        form.instance.save()
        perfil.save()

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
