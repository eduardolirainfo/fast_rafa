from typing import Optional

from pydantic import BaseModel


class OrganizacaoSchema(BaseModel):
    id: Optional[int]
    nome: str

    class Config:
        from_attributes = True
