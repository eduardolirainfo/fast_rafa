from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .user import UserSchema


class PostSchema(BaseModel):
    id: Optional[int]
    titulo: str
    conteudo: str
    urlImagem: Optional[str] = None
    criadoEm: Optional[datetime] = None
    atualizadoEm: Optional[datetime] = None
    idUsuario: int

    @property
    def usuario(self):
        return UserSchema(id=self.idUsuario)

    @staticmethod
    def get_all() -> list:
        return []
