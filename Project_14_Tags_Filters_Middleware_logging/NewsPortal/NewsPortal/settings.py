"""
Django settings for NewsPortal project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9s5^fldp01@@!6ei++x!=!fgnemc$j#r09bos$)p_r8wema9ec'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'style' : '{',
    'formatters': {
        'format_1': {
            'format': '%(asctime)s %(levelname)s %(message)s'
        },
        'format_2': {
            "format": '%(asctime)s %(levelname)s %(message)s %(pathname)s'
        },
        'format_3': {
            "format": '%(asctime)s %(levelname)s %(message)s %(pathname)s %(exc_info)s'
        },
        'format_4': {
            "format": '%(asctime)s %(levelname)s %(module)s %(message)s'
        },
        'format_5': {
            "format": '%(asctime)s %(levelname)s %(message)s %(pathname)s %(exc_info)s'
        },
        'format_6': {
            "format": '%(asctime)s %(levelname)s %(message)s %(pathname)s'
        }
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console_d': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'format_1'
        },
        'console_w': {
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'format_2'
        },
        "console_e":{
            'level': "ERROR",
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'format_3'
        },
        "console_c":{
            'level': "CRITICAL",
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'format_3'
        },
        'file_i': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'formatter': 'format_4',
            "filename": "general.log"
        },
        'file_e': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.FileHandler',
            'formatter': 'format_5',
            "filename": "errors.log"
        },
        'file_c': {
            'level': 'CRITICAL',
            'filters': ['require_debug_true'],
            'class': 'logging.FileHandler',
            'formatter': 'format_5',
            "filename": "errors.log"
        },
        "file_security":{
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filters': ['require_debug_true'],
            "filename": "security.log",
            "formatter": "format_4"
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            "formatter": "format_6"
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console_d', "console_w", "console_e", "console_c", "file_i"],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins', "file_e", "file_c"],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['mail_admins', "file_e", "file_c"],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.template': {
            'handlers': ["file_e", "file_c"],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ["file_e", "file_c"],
            'level': 'DEBUG',
            'propagate': False,
        },
        "django.security": {
            "handlers": ["file_security"],
            'level': 'DEBUG',
            'propagate': False,
        }
    }
}



ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'django.contrib.flatpages',

    'accounts',
    'news',

    'django_filters',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',

    'django_apscheduler'
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_CONFIRM_EMAIL_ON_GET = False
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1

ACCOUNT_FORMS = {"signup": "accounts.forms.CustomSignupForm"}

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',

    # 'django.middleware.cache.UpdateCacheMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'NewsPortal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'django.template.context_processors.request'
            ],
        },
    },
]
# CACHE
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
        'TIMEOUT': 30,
        # Указываем, куда будем сохранять кэшируемые файлы! Не забываем создать папку cache_files внутри папки с manage.py!
    }
}
# Этого раздела может не быть, добавьте его в указанном виде.
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'NewsPortal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CELERY
t_login = "default"
t_password = "kKFfyMH2yroVjzEi79CNGu2CqToNgLOR"
t_endpoint = "redis-16821.c135.eu-central-1-1.ec2.cloud.redislabs.com:16821"

CELERY_BROKER_URL = f"redis://{t_login}:{t_password}@{t_endpoint}"
CELERY_RESULT_BACKEND = f"redis://{t_login}:{t_password}@{t_endpoint}"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#_______________

LOGIN_REDIRECT_URL = "/news"

LOGOUT_REDIRECT_URL= "/news"

#_______________________
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = "porquenosaber@yandex.ru"
EMAIL_HOST_PASSWORD = "joamnrtouevcsigk"
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = "porquenosaber@yandex.ru"

SERVER_EMAIL = "example@yandex.ru"
MANAGERS = (
    ('Ivan', 'porquenosaber@yandex.ru'),
    ('Petr', 'porquenosaber@yandex.ru'),
)
ADMINS = (
    ('anton', 'porquenosaber@yandex.ru'),
)