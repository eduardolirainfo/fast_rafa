from pydantic import BaseModel


class TokenData(BaseModel):
    username: str | None = None


class Auth(BaseModel):
    access_token: str
    token_type: str = 'bearer'
