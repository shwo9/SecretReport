from .common import *

INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

INTERNAL_IPS = ["127.0.0.1",
                "*"]


ALLOWED_HOSTS = [
    "115.145.154.101",
    "127.0.0.1",
    '.ap-northeast-2.compute.amazonaws.com',
    "*",
    "0.0.0.0",
]
