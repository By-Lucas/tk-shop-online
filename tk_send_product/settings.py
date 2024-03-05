import os
import sys
from pathlib import Path
from loguru import logger
from decouple import config, Csv
from django.contrib.messages import constants


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

logger.add("logs/logs.log",  serialize=False)
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>", backtrace=True, diagnose=True)
logger.opt(colors=True)

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Se o ambiente é 'prod', usa a URL de produção. Caso contrário, usa a URL de QA.
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', cast=Csv())

# Application definition
APPS_DIR = sys.path.append(os.path.join(BASE_DIR, 'apps'))

DJANGO_APPS = [
    'jet.dashboard',
    'jet', 
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
]

PROJECT_APPS = [
    'ads',
    'core',
    'stores',
    'config',
    'company',
    'accounts',
    'products',
    'category',
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tk_send_product.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                'apps.config.context_processors.get_ads',
                'apps.config.context_processors.get_category',
                'apps.config.context_processors.get_config_site',
                'apps.config.context_processors.get_social_media',
                'apps.config.context_processors.get_company_stores',
                'apps.config.context_processors.get_company_profile',
            ],
        },
    },
]

WSGI_APPLICATION = 'tk_send_product.wsgi.application'


# Database
DB_NAME= config('DB_NAME')
SCHEMA_DB= config('SCHEMA_DB')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# Habilitar segurança SSL para banco externos(não usar em localhost) + Schema do banco selecionado de acordo com tipo de ambiente
#DATABASES['default']['OPTIONS'] = {'sslmode': 'require', 'options': f'-c search_path=tk_copyfx,{SCHEMA_DB}'}  
DATABASES['default']['OPTIONS'] = {'options': f'-c search_path={DB_NAME},{SCHEMA_DB}'} 

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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# TAGS MESSAGE TEMPLATE
MESSAGE_TAGS = {
    constants.DEBUG: 'primary',
    constants.ERROR: 'danger',
    constants.SUCCESS: 'success',
    constants.INFO: 'info',
    constants.WARNING: 'warning',
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django_debug.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

############################ IMPORTAR OUTRAS CONFIGURAÇÕES ############################
from .config_main import *
####################################################################################

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
