"""
Django settings for barbados project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+tvselzienz_7qyd16a#ir+_(kn)@r38)v_qhoes$$(pvznv))'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [
    '127.0.0.1',
]


# Application definition

INSTALLED_APPS = (
    # 'admin_tools',
    # 'admin_tools.theming',
    # 'admin_tools.menu',
    # 'admin_tools.dashboard',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pipeline',
    'django_extensions',
    'barbados.barbadosdb',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'pipeline.middleware.MinifyHTMLMiddleware',
)

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
                'django.core.context_processors.csrf',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.request',
                'django.core.context_processors.static',
                'django.core.context_processors.tz',
            ],
        },
    },
]


ROOT_URLCONF = 'barbados.urls'

WSGI_APPLICATION = 'barbados.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'barbados',
    }
}

# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'


# Codento-specifics

# ADMIN_TOOLS_INDEX_DASHBOARD = 'barbados.dashboard.CustomIndexDashboard'
# ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'barbados.dashboard.CustomAppIndexDashboard'

STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

# XXX: Set the REQUEST_LOG path to something
REQUEST_LOG = 'request.log'
REQUEST_LOG_LEVEL = os.getenv('REQUEST_LOG_LEVEL', 'INFO')
REQUEST_LOG_MAX_BYTES = 8388608

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'class': 'barbados.logging.handlers.GroupWriteRotatingFileHandler',
            'backupCount': 10,
            'maxBytes': REQUEST_LOG_MAX_BYTES,
            'filename': REQUEST_LOG,
            'level': REQUEST_LOG_LEVEL,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': REQUEST_LOG_LEVEL,
            'propagate': True,
        },
    },
}

