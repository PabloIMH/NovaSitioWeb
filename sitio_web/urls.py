from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from desarrollo import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # Página de inicio (home)
    path('', views.home, name='home'),

    # Administrador
    path('admin/', admin.site.urls),

    # Inicio de sesión personalizado
    path('login/', views.custom_login, name='custom_login'),  # Aquí se usa la vista personalizada para el login

    # Página del cliente
    path('cliente/', views.cliente_view, name='cliente_view'),  # Cambiar el nombre a 'cliente_view' para ser consistente

    # Rutas para el manejo de la recuperación de contraseñas
<<<<<<< HEAD
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="registration/password_reset.html"), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="registration/password_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_confirm.html"), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_complete.html"), name='password_reset_complete'),
    
    # Rutas para el manejo de la recuperación de contraseñas predeterminadas
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset_done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]



=======
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

>>>>>>> 25e93f093e206db20e455f818b79879b40b47eb9
# Servir archivos estáticos y de medios en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
