import logging

from fastapi import Depends, APIRouter

from app import schemas, auth


logger = logging.getLogger(__name__)
api = APIRouter(tags=['Auth'])


@api.post('/token/', response_model=schemas.CredentialData)
def login(user: schemas.UserDB = Depends(auth.get_current_active_user_token_auth)):
    return schemas.CredentialData(access_token=auth.encode_token(user))
