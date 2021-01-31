import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", '')

ENCRYPT_KEY = os.environ.get("ENCRYPT_KEY", '')

DEBUG = False

ALLOWED_HOSTS = ['ajaysharma96.pythonanywhere.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangong',
        'USER': os.environ.get("MYAPP_DB_USER", ''),
        'PASSWORD': os.environ.get("MYAPP_DB_PASSWORD", ''),
        'HOST': 'ajaysharma96.mysql.pythonanywhere-services.com',
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get("MYAPP_EMAIL_USER", '')
EMAIL_HOST_PASSWORD = os.environ.get("MYAPP_EMAIL_PASSWORD", '')
EMAIL_PORT = 587

CORS_ORIGIN_WHITELIST = [
    'https://creativeweb-3a289.web.app',
    'https://ajaysharma96.pythonanywhere.com'
]

CORS_ORIGIN_REGEX_WHITELIST = [
    'https://creativeweb-3a289.web.app/',
    'https://ajaysharma96.pythonanywhere.com/'
]

MEDIA_ROOT = '/home/ajaysharma96/DjangoProject/media'
MEDIA_URL = '/media/'
STATIC_ROOT = '/home/ajaysharma96/DjangoProject/static'
STATIC_URL = '/static/'