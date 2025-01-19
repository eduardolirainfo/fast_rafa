from typing import Optional

from pydantic import BaseModel


class TokenData(BaseModel):
    username: Optional[str] = None


class Auth(BaseModel):
    access_token: str
    token_type: str = 'bearer'
