DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'invest_api',
        'USER': 'invest_api',
        'PASSWORD': 'invest_api',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
ALLOWED_HOSTS = ['']

STATIC_URL = '/assets/'
DEBUG = 1
