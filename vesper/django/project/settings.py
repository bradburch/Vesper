"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/

For a Django deployment checklist, see
https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/
"""


from pathlib import Path

from environs import Env, EnvError

import vesper.util.logging_utils as logging_utils


# Configure logging for Vesper server early, before anybody logs anything.
logging_utils.configure_root_logger()


# Read .env file and environment variables.
env = Env()
env.read_env('Environment Variables.env', recurse=False)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: Never put the actual secret key here.
SECRET_KEY = env('VESPER_DJANGO_SECRET_KEY')

# SECURITY WARNING: Don't run with debug turned on in production.
DEBUG = env.bool('VESPER_DJANGO_DEBUG', False)

ALLOWED_HOSTS = env.list(
    'VESPER_DJANGO_ALLOWED_HOSTS',
    ['.localhost', '127.0.0.1', '[::1]'], subcast=str)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'vesper.django.app.apps.VesperConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vesper.django.project.urls'

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

WSGI_APPLICATION = 'vesper.django.project.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

# TODO: Switch to BigAutoField when Vesper database tables will change
# for some other reason. We don't want to force users to migrate their
# databases just for this. There's no hurry, since it is unlikely that
# any archive database table will exhaust 2**32 IDs anytime soon.
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


# The path of the Vesper archive directory, by default the current
# working directory.
#
# We define this attribute here instead of at the end of this file
# so we can use it in the default database URL, below.
VESPER_ARCHIVE_DIR_PATH = env.path('VESPER_ARCHIVE_DIR_PATH', '/Archive')

# The URL of the Vesper archive database, by default the URL of the
# SQLite database in the file "Archive Database.sqlite" of the Vesper
# archive directory.
#
# See https://github.com/jazzband/dj-database-url for the form of
# URLs for various kinds of databases.
VESPER_ARCHIVE_DATABASE_URL = env.dj_db_url(
    'DATABASE_URL',
    f'sqlite:///{VESPER_ARCHIVE_DIR_PATH}/Archive Database.sqlite')


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    'default': VESPER_ARCHIVE_DATABASE_URL
}


# The paths of the Vesper archive recording directories.
#
# The value of this settintg is used by the `VesperConfig` class
# to initialize `archive_paths.recording_dir_paths`.
try:
    VESPER_RECORDING_DIR_PATHS = \
        env.list('VESPER_RECORDING_DIR_PATHS', subcast=Path)

except EnvError:
    # environment variable not defined

    VESPER_RECORDING_DIR_PATHS = None

    
VESPER_ARCHIVE_READ_ONLY = env.bool('VESPER_ARCHIVE_READ_ONLY', True)
