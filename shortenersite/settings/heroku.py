from .common import *  # noqa

SECRET_KEY = env('DJANGO_SECRET_KEY')


DATABASES = {
    # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
    'default': env.db(),
}

DEBUG = False
