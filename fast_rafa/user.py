from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, constr

from .favorito import FavoriteSchema


class UserSchema(BaseModel):
    organizacaoId: int
    eNaoGovernamental: bool
    eGerente: bool
    primeiroNome: constr(max_length=50)
    sobrenome: constr(max_length=50)
    email: EmailStr
    telefone: constr(max_length=20)
    dataNascimento: date
    eSurdo: Optional[bool] = None
    usaCadeiraDeRodas: Optional[bool] = None
    temDeficienciaCognitiva: Optional[bool] = None
    eLgbtq: Optional[bool] = None
    urlImagemPerfil: constr(max_length=2048)
    senhaHash: constr(max_length=255)
    favoritos: List[FavoriteSchema] = []
    criadoEm: Optional[datetime] = None
    atualizadoEm: Optional[datetime] = None

    @property
    def favorito(self):
        return [f for f in FavoriteSchema.get_all() if f.idUsuario == self.id]


class UserPublic(BaseModel):
    id: int
    organizacaoId: int
    eNaoGovernamental: bool
    eGerente: bool
    primeiroNome: constr(max_length=50)
    sobrenome: constr(max_length=50)
    email: EmailStr
    telefone: constr(max_length=20)
    dataNascimento: date
    eSurdo: Optional[bool] = None
    usaCadeiraDeRodas: Optional[bool] = None
    temDeficienciaCognitiva: Optional[bool] = None
    eLgbtq: Optional[bool] = None
    urlImagemPerfil: constr(max_length=2048)
    favoritos: List[FavoriteSchema] = []
    criadoEm: Optional[datetime] = None
    atualizadoEm: Optional[datetime] = None

    @property
    def favorito(self):
        return [f for f in FavoriteSchema.get_all() if f.idUsuario == self.id]


class UserDb(UserSchema):
    id: Optional[int]


class UserList(BaseModel):
    users: List[UserPublic]
