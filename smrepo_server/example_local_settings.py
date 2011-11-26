import settings

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'plugins.db.sq3',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

SECRET_KEY = ''

if settings.TEST_MODE:
    DEBUG = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'plugins.db.sq3',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }
    
    if DATABASES['default']['ENGINE'] == 'django.db.backends.mysql':
        DATABASES['default']['OPTIONS'] = {
           "init_command": "SET storage_engine=INNODB",
        }

