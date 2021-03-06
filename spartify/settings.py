"""
Django settings for spartify project.

Generated by 'django-admin startproject' using Django 2.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from dotenv import load_dotenv
load_dotenv()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DEBUG", default=1))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS",'').split(" ") + ['*', '192.168.43.72', '192.168.0.53', '0.0.0.0']

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.spotify.SpotifyOAuth2',
)

AUTH_USER_MODEL = 'backend.User'
SOCIAL_AUTH_USER_MODEL = 'backend.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'social_django',
    'backend',
    'lobby'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'backend.middlewares.ApiMiddleware',
]

ROOT_URLCONF = 'spartify.urls'

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

WSGI_APPLICATION = 'spartify.wsgi.application'
ASGI_APPLICATION = 'spartify.routing.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("SQL_USER", "user"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = 'staticfiles/'
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL)

SOCIAL_AUTH_SPOTIFY_KEY = os.environ['SOCIAL_AUTH_SPOTIFY_KEY']  
SOCIAL_AUTH_SPOTIFY_SECRET = os.environ['SOCIAL_AUTH_SPOTIFY_SECRET'] 
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_SPOTIFY_SCOPE = ['user-read-email','user-read-private', 'user-read-playback-state', 'user-modify-playback-state']
# SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'http://{}/complete/spotify/' % os.getenv('HOST')

LOGIN_REDIRECT_URL = 'dashboard'
LOGIN_URL = 'login'

DEFAULT_AUTO_FIELD='django.db.models.AutoField'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'backend.pipeline.save_access_token', #save token on login,
)

QUEUE_SESSION_ID = 'queue'
SESSION_EXPIRE_AT_BROWSER_CLOSE = 15


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'api_formatter': {
            'format': '{username} -- {endpoint} -- {status_code:d}: {message}',
            'style': '{',
        },
        'lobby_formatter': {
            'format': '{id}--{username}: {message} -- {asctime}',
            'style': '{',
        },
    },
    'handlers': {
        'api_errors': {
            'class': 'logging.FileHandler',
            'filename': 'logs/api_errors.log',
            'formatter': 'api_formatter',
            'level': 'ERROR',
        },
    },
    'loggers':{
        'backend': {
            'handlers': ['api_errors'],
        },
    },
}


REDIS_HOST = os.environ.get("REDIS_HOST", '127.0.0.1')
REDIS_PORT = 6379
REDIS_DB = 0

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    }
}