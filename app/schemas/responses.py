from pydantic import BaseModel


class OkResponse(BaseModel):
    status: str = 'ok'


class CredentialData(BaseModel):
    access_token: str
    token_type: str = 'bearer'
