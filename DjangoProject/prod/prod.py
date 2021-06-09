import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "a_eit*qp51vgq0f8c9c@o_nozqrij%n%#(l6!$gy6fguj2sxp!")

ENCRYPT_KEY = os.environ.get("ENCRYPT_KEY")

DEBUG = False

ALLOWED_HOSTS = [
    os.environ.get('ALLOWED_HOST')
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get("DATABASE_USERNAME"),
        'PASSWORD': os.environ.get("DATABASE_PASSWORD"),
        'HOST': os.environ.get('DATABASE_HOST'),
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get("EMAIL_ID")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_PASSWORD")
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
