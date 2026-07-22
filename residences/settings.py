from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================
# SECURITY
# =========================

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-^c&$ck^*e8l1o4w1%i+bq*ijh#j85734-5n#wdox=n6d+@f3_$"
)

DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = os.environ.get(
    "ALLOWED_HOSTS",
    "127.0.0.1,localhost"
).split(",")

CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
]


# =========================
# APPLICATIONS
# =========================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'whitenoise.runserver_nostatic',

    'core',
]


# =========================
# MIDDLEWARE
# =========================

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


ROOT_URLCONF = 'residences.urls'


# =========================
# TEMPLATES
# =========================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [

                'django.template.context_processors.request',

                'django.contrib.auth.context_processors.auth',

                'django.contrib.messages.context_processors.messages',

                'core.context_processors.global_settings',

            ],
        },
    },
]


WSGI_APPLICATION = 'residences.wsgi.application'


# =========================
# DATABASE
# LOCAL + RENDER
# =========================

DATABASE_URL = os.environ.get("DATABASE_URL")


if DATABASE_URL:

    # Base PostgreSQL Render
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }

else:

    # Base PostgreSQL locale
    DATABASES = {
        "default": {

            "ENGINE": "django.db.backends.postgresql",

            "NAME": "residences_db",

            "USER": "postgres",

            "PASSWORD": "MET_TON_MOT_DE_PASSE_POSTGRES",

            "HOST": "localhost",

            "PORT": "5432",

        }
    }



# =========================
# PASSWORD VALIDATION
# =========================

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


# =========================
# LOCALISATION
# =========================

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Africa/Abidjan'

USE_I18N = True

USE_TZ = True



# =========================
# STATIC
# =========================

STATIC_URL = '/static/'


STATICFILES_DIRS = [
    BASE_DIR / 'core' / 'static',
]


STATIC_ROOT = BASE_DIR / 'staticfiles'


STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)



# =========================
# MEDIA
# =========================

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'



# =========================
# DEFAULT PK
# =========================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# =========================
# LOGIN
# =========================

LOGIN_URL = 'connexion'

LOGIN_REDIRECT_URL = 'accueil'



# =========================
# EMAIL
# =========================

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'



# =========================
# WHATSAPP
# =========================

WHATSAPP_NUMBER = "2250778485274"