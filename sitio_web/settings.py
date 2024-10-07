from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9qlk#y5+m3mw%-#!rs262nvp3cttdv!m3^k=n8=j74_32kc93i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'desarrollo',
    'django_cleanup.apps.CleanupConfig',  # Limpia automáticamente los archivos no usados (para las imágenes de perfil)
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Agregado para habilitar traducciones
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sitio_web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'sitio_web.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nova_analytics',
        'USER': 'user_nova',
        'PASSWORD': 'nova123',
        'HOST': 'localhost',  
        'PORT': '5432',     
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'es'  # Cambiado a español

TIME_ZONE = 'America/Santiago'  # Cambiado a la zona horaria de Chile

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / 'locale',  # Definir ruta para archivos de traducción si usas gettext
]


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'sitio_web', 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (para cargar imágenes de perfil de usuario)
import os

# Configuración para archivos media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de correo
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'reclaprosgie@gmail.com'
EMAIL_HOST_PASSWORD = 'z r m y p j t f w g u u z u l f'
DEFAULT_FROM_EMAIL = 'reclaprosgie@gmail.com'


# Configuración de autenticación
AUTHENTICATION_BACKENDS = [
    'desarrollo.backends.EmailOrUsernameBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Redirección tras el login y logout
LOGIN_REDIRECT_URL = '/admin/'  # Redirigir al panel de administración tras iniciar sesión si es administrador
LOGOUT_REDIRECT_URL = '/'  # Redirigir al home después de cerrar sesión

AUTHENTICATION_BACKENDS = (
    'desarrollo.backends.EmailOrUsernameBackend',  # Asegúrate de que apunte correctamente a tu archivo 'backends.py'
    'django.contrib.auth.backends.ModelBackend',  # Mantén el backend predeterminado también
)

JAZZMIN_SETTINGS = {
    "site_title": "Nova Analytics Admin",
    "site_header": "Nova Analytics",
    "site_brand": "Nova Analytics",  # Texto en la barra superior
    "welcome_sign": "Bienvenido al panel de administración",
    "show_sidebar": True,
    "navigation_expanded": True,

    # Orden de las aplicaciones
    "order_with_respect_to": ["auth", "books", "book_issues"],

    # Iconos personalizados
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },

    # Configuración del logo
    "site_logo_small": "img/logo.png",  # Un logo alternativo para el menú colapsado (opcional)
    "site_logo_"
    "site_logo_classes": "img-circle",  # Clase CSS para personalizar el logo

    # Mostrar u ocultar el botón de personalización de UI de Jazzmin
    "show_ui_builder": False,  # Si no quieres mostrar el botón del UI builder en el admin
}
