from typing import Optional

from pydantic import BaseModel


class ListaDeInteresseSchema(BaseModel):
    id: Optional[int]
    nome: str

    class Config:
        from_attributes = True
