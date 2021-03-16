import os

SECRET = os.environ.get('SECRET', '')
PROD = os.environ.get('ENV', 'dev') == 'prod'
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'db')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'db')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'db_user')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'password')
SENTRY_DSN = os.environ.get('SENTRY_DSN')
SA_POOL_SIZE = int(os.environ.get('SA_POOL_SIZE', 4))
SA_MAX_OVERFLOW = int(os.environ.get('SA_MAX_OVERFLOW', 1))
