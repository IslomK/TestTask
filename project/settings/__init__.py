from .base import *

IS_PRODUCTION = int(os.getenv('IS_PRODUCTION', 0))

if IS_PRODUCTION:
    from .production import *
