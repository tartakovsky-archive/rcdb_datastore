from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from db.sessions import session
from .views import api

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
