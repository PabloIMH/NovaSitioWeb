from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .forms import CustomUserCreationForm
import logging

class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserCreationForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),  # Campos generales
        ('Información personal', {'fields': ('first_name', 'last_name')}),  # Información del usuario
        ('Permisos', {'fields': ('is_staff', 'is_superuser')}),  # Campos de permisos
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'rol'),  # Añadimos 'rol'
        }),
    )
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not obj:  # Si estamos añadiendo un nuevo usuario
            # Generar la contraseña automáticamente
            random_password = get_random_string(length=12)
            form.base_fields['password1'].initial = random_password
            form.base_fields['password2'].initial = random_password
            form.base_fields['password1'].disabled = True  # Deshabilitar el campo para que no pueda ser editado
            form.base_fields['password2'].disabled = True
        return form

    def save_model(self, request, obj, form, change):
        if not change:  # Si es un usuario nuevo
            random_password = form.cleaned_data['password1']
            obj.set_password(random_password)  # Asignar la contraseña generada
            
            # Asignar el rol
            rol = form.cleaned_data.get('rol')
            if rol == 'superadmin':  # Cambia 'admin' por 'superadmin'
                obj.is_staff = True  # Administrador
                obj.is_superuser = True  # Administrador tendrá acceso total como superusuario
            else:
                obj.is_staff = False  # Cliente (suscriptor)
                obj.is_superuser = False  # No es superusuario
            
            # Guardar el usuario antes de enviar el correo
            obj.save()
            
            # Enviar el correo con la contraseña generada
            send_mail(
                'Tu cuenta ha sido creada en el sistema',
                f'Tu nombre de usuario es {obj.username} y tu contraseña temporal es {random_password}',
                'noreply@tu-sitio.com',  # Cambia el remitente
                [obj.email],
                fail_silently=False,
            )
        else:
            super().save_model(request, obj, form, change)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
