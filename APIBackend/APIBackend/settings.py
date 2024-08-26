"""
Django settings for APIBackend project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from mongoengine import connect
from pathlib import Path
# Celery Configuration Options
CELERY_TIMEZONE = "Africa/Nairobi"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
# CELERY_BROKER_URL = 'amqp://localhost'
CELERY_BROKER_URL = 'amqp://guest:guest@rabbitmq:5672/'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'

# scheduler
CELERY_BEAT_SCHEDULE = {
      'add-every-30-seconds': {
        'task': 'APIBackend.tasks.add_two_numbers',
        'schedule': 5.0,
        'args': (16, 16),
        'options': {
            'expires': 15.0,
        },
    },
}

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
APPEND_SLASH=False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-vn(b-e)^#doqv-z94qx5kx+0==7-m*74dbhow2*(=$t&=)%^(!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', 
    'corsheaders',
    'SentimentAnalysis.apps.SentimentanalysisConfig',
    'django_celery_results',
    
]

CORS_ORIGIN_ALLOW_ALL = True

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'APIBackend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'APIBackend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
MONGODB_SETTINGS = {
    'db': 'kq_database',
    'host': 'mongodb+srv://silomalojoseph:DKSQyFwZd4W4UFF2@testing.p4yxv.mongodb.net/kq_database?retryWrites=true&w=majority&appName=testing',
    'username': 'silomalojoseph',
    'password': 'DKSQyFwZd4W4UFF2',
    'authentication_source': 'admin',
    'authMechanism': 'SCRAM-SHA-1'
}

# Connect to MongoDB
connect(**MONGODB_SETTINGS)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    # 'default': {
    #     'ENGINE': 'djongo',
    #     'CLIENT': {
    #         "host": "mongodb+srv://silomalojoseph:DKSQyFwZd4W4UFF2@testing.p4yxv.mongodb.net/?retryWrites=true&w=majority&appName=testing",
    #         "name": "kq_database",
    #         "authMechanism": "SCRAM-SHA-1"
    #         }
    # }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
