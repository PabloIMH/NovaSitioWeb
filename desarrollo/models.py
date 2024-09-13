from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)

    # Agregamos el campo "rol" para distinguir entre Administrador y Suscriptor
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('suscriptor', 'Suscriptor'),
    ]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='suscriptor')

    def __str__(self):
        return self.user.username

# Crear el perfil de usuario automáticamente al crear un usuario
@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)

# Guardar automáticamente el perfil cuando se guarda el usuario
@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    try:
        instance.perfilusuario.save()
    except PerfilUsuario.DoesNotExist:
        PerfilUsuario.objects.create(user=instance)
