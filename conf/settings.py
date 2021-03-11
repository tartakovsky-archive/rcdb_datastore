import os

PROD = os.environ.get('ENV', 'dev') == 'prod'
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'db')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'db')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'db_user')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'password')
SENTRY_DSN = os.environ.get('SENTRY_DSN')
