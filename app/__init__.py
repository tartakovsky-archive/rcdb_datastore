import logging


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from uvicorn.config import LOGGING_CONFIG

from db.sessions import session
from conf.settings import PROD, SENTRY_DSN
from conf.sentry import init_sentry
from .views import api

logging.basicConfig(
    format='[%(asctime)s] %(name)s [%(levelname)s] %(message)s',
    level=logging.DEBUG
)
LOGGING_CONFIG["formatters"]["access"]["fmt"] = '[%(asctime)s] %(name)s [ACCESS] %(client_addr)s - "%(request_line)s" %(status_code)s'

logging.info(f'Starting app with PROD:{PROD}')

app = FastAPI(docs_url='/', title='Datastore')
app.include_router(api)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.middleware('http')
async def rollback_alchemy(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.remove()


if PROD:
    if SENTRY_DSN:
        init_sentry(SENTRY_DSN)
        app = SentryAsgiMiddleware(app)
