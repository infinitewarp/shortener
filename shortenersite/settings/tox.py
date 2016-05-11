from tempfile import mkdtemp

from .common import *  # noqa

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY',
                 default="*wz-4@4(r$!pe2j85kta5ks&4bl(hef9hty)%a-(i0d3c0uyf%")

# tox should always have its own temporary database
# TODO allow an easier way to override this?
temp_sqlite3_dir = mkdtemp()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(temp_sqlite3_dir, 'db.sqlite3'),
    }
}

DEBUG = True
