import os


class Common:
    """
    Common settings class. All children derived from this one.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    ITEMS_PER_PAGE = 20
    GITHUB_REPOSITORY_URL = 'https://api.github.com/search/repositories'
    CELERY_BROKER_URL = 'redis://redis:6379/1'
    CELERY_RESULT_BACKEND = 'redis://redis:6379/1'


class Dev(Common):
    """
    Development settings.
    """
    DEBUG = True
    MONGODB_SETTINGS = {
        'db': 'api',
        'host': 'mongo',
        'port': 27017
    }
