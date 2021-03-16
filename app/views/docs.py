from fastapi import APIRouter, Depends, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from app import schemas
from app import auth

api = APIRouter(include_in_schema=False)


@api.get('/')
def get_documentation(user: schemas.UserDB = Depends(auth.get_current_active_user_basic_auth)):
    return get_swagger_ui_html(openapi_url='/openapi.json', title='docs')


@api.get('/openapi.json')
def openapi(request: Request, username: schemas.UserDB = Depends(auth.get_current_active_user_basic_auth)):
    return get_openapi(title='Datastore', version='0.1.0', routes=request.app.routes)
