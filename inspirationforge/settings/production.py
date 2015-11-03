from .base import *

DEBUG = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_ROOT = get_secret("MEDIA_ROOT")

# Security-related settings
ALLOWED_HOSTS = [".inspirationforge.com"]
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

