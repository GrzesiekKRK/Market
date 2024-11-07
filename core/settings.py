from pathlib import Path
import os

# TODO remove boilerplate comments
# TODO add pre-commit like in Cipher project.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv('django')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_EXTENSIONS = [
    'cart',
    'deliveries',
    'inventories',
    'notifications',
    'orders',
    'payments',
    'products',
    'users',
    'wishlists',
    ]

INSTALLED_APPS += INSTALLED_EXTENSIONS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'users.context_processors.roles',
                'cart.context_processors.items_number',
                'notifications.context_processors.messages_number',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'MarketDB',
        'USER': 'postgres',
        # 'USER': 'MarketOwner',
        # 'PASSWORD': 'myPassWordDEi',
        'PASSWORD': '9261',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')


MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.CustomUser'
CART_SESSION_ID = 'cart'


LOGIN_REDIRECT_URL = '/login'


STRIPE_PUBLISHABLE_KEY = 'pk_test_51PETcT05Gsg5Ch9YFmXTCMQ38hITal9A2aSlxIQOB72STArVKxFBveoviEA7WRsK8oGiTZP1yjkWVwA4TgCrR2yp009bQ4AyAh'
STRIPE_SECRET_KEY = os.getenv('STRIPE_TEST_KEY')
STRIPE_ENDPOINT_SECRET = os.getenv('STRIPE_ENDPOINT_SECRET')

