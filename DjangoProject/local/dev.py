import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

ENCRYPT_KEY = os.environ.get("ENCRYPT_KEY")

DEBUG = True

ALLOWED_HOSTS = [
    os.environ.get('ALLOWED_HOST')
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USERNAME'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT')
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'djangong',
#         'USER': 'root',
#         'PASSWORD': '143136420',
#         'HOST': 'localhost',
#         'PORT': '3306'
#     }
# }

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get("EMAIL_ID")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")
EMAIL_PORT = 587

CORS_ORIGIN_WHITELIST = [
    'http://localhost',
    'http://192.168.1.42',
    'http://192.168.1.104',
    'http://192.168.1.102'
]

CORS_ORIGIN_REGEX_WHITELIST = [
    'http://localhost:4200',
    'http://192.168.1.42:4200',
    'http://192.168.1.104:4200',
    'http://192.168.1.102:4200'
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
