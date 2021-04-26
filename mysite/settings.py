from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '(k-cyql8w(!l4%%ro+pqh3bl70!-q@idgn@&aq0^s6iv#a1i8=')

DEBUG = bool( os.environ.get('DJANGO_DEBUG', True))


ALLOWED_HOSTS = ['127.0.0.1', 'nameless-crag-89185.herokuapp.com']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'shop.apps.ShopConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrdersConfig',
    'django_cleanup',
    'blog.apps.BlogConfig',
    'accounts.apps.AccountsConfig',
    'crispy_forms',
    'storages',

]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

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
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'graduateworkdb',
        'USER': 'maksim',
        'PASSWORD': 'qwerty111',
        'HOST': 'localhost',
        'PORT': '5432',
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



LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True



AWS_ACCESS_KEY_ID = 'AKIA56V4ARNB2BXARW4R'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'pran-grad'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)


db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

CART_SESSION_ID = 'cart'

GOOGLE_RECAPTCHA_SITE_KEY = '6Lfbm2YaAAAAAGzzUyF-aVYT5TtUQZQV-bo3IpW7'
GOOGLE_RECAPTCHA_SECRET_KEY = '6Lfbm2YaAAAAAJsy5_kYjOzT247W30QP3i7HTe1b'

