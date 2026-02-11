from .base import *


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': os.getenv("DB_ENGINE", default="django.db.backends.sqlite3"),
        'NAME': os.getenv("DB_NAME", default=BASE_DIR / "db.sqlite3"),
        'USER': os.getenv("DB_USER", default="user"),
        'PASSWORD': os.getenv("DB_PASSWORD", default="password"),
        'HOST': os.getenv("DB_HOST", default="localhost"),
        'PORT': os.getenv("DB_PORT", default="5432"),
    }
}
