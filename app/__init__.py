import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from uvicorn.config import LOGGING_CONFIG

from app import views
from conf.settings import PROD, SENTRY_DSN
from conf.sentry import init_sentry


logging.basicConfig(
    format='[%(asctime)s] %(name)s [%(levelname)s] %(message)s',
    level=logging.DEBUG
)
ACCESS_LOG_FMT = '[%(asctime)s] %(name)s [ACCESS] %(client_addr)s - "%(request_line)s" %(status_code)s'
LOGGING_CONFIG["formatters"]["access"]["fmt"] = ACCESS_LOG_FMT

logging.info(f'Starting app with PROD:{PROD}')

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.include_router(views.auth.api)
app.include_router(views.log.api)
app.include_router(views.docs.api)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


if PROD:
    if SENTRY_DSN:
        init_sentry(SENTRY_DSN)
        app = SentryAsgiMiddleware(app)
