import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a_eit*qp51vgq0f8c9c@o_nozqrij%n%#(l6!$gy6fguj2sxp!'

ENCRYPT_KEY = b'2TRwuyTh2qAY3PzZgXU6q8Sqqmdsw_eCvvTG1B_LuYo='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangong',
        'USER': 'debian-sys-maint',
        'PASSWORD': 'pLOpkbGobXinFZsP',
        'HOST': 'localhost',
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'ajaysharmadevelopment@gmail.com'
EMAIL_HOST_PASSWORD = 'dqdaiwwnopvqjidy'
EMAIL_PORT = 587

CORS_ORIGIN_WHITELIST = [
    'http://192.168.1.11',
    'http://127.0.0.1',
    'http://localhost:4200'
]

CORS_ORIGIN_REGEX_WHITELIST = [
    'http://192.168.1.11:4200',
    'http://localhost:4200',
    'http://127.0.0.1:4200'
]

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
