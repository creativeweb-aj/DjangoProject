import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = os.environ.get("SECRET_KEY", 'a_eit*qp51vgq0f8c9c@o_nozqrij%n%#(l6!$gy6fguj2sxp!')
SECRET_KEY = 'a_eit*qp51vgq0f8c9c@o_nozqrij%n%#(l6!$gy6fguj2sxp!'

# ENCRYPT_KEY = os.environ.get("ENCRYPT_KEY", "b'2TRwuyTh2qAY3PzZgXU6q8Sqqmdsw_eCvvTG1B_LuYo='")
ENCRYPT_KEY = b'2TRwuyTh2qAY3PzZgXU6q8Sqqmdsw_eCvvTG1B_LuYo='

DEBUG = False

ALLOWED_HOSTS = ['ajaysharma96.pythonanywhere.com']

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ajaysharma96$djangong',
        # 'USER': os.environ.get("MYAPP_DB_USER", 'ajaysharma96'),
        'USER': 'ajaysharma96',
        # 'PASSWORD': os.environ.get("MYAPP_DB_PASSWORD", 'Pass143136'),
        'PASSWORD': 'Pass143136',
        'HOST': 'ajaysharma96.mysql.pythonanywhere-services.com',
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = os.environ.get("MYAPP_EMAIL_USER", 'ajaysharmadevelopment@gmail.com')
EMAIL_HOST_USER = 'ajaysharmadevelopment@gmail.com'
# EMAIL_HOST_PASSWORD = os.environ.get("MYAPP_EMAIL_PASSWORD", 'dqdaiwwnopvqjidy')
EMAIL_HOST_PASSWORD = 'dqdaiwwnopvqjidy'
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