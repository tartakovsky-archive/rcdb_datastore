from fastapi import FastAPI, Request

from db.sessions import session
from .views import api

app = FastAPI(docs_url='/')
app.include_router(api)


@app.middleware('http')
async def rollback_alchemy(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.remove()
