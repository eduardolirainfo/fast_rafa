from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EventCreate(BaseModel):
    id_organizacao: int
    id_usuario: int
    fechado: datetime
    titulo: str
    descricao: str
    data: datetime
    url_imagem: Optional[str]


class EventUpdateRequest(BaseModel):
    id_organizacao: Optional[int]
    id_usuario: Optional[int]
    fechado: Optional[datetime]
    titulo: Optional[str]
    descricao: Optional[str]
    data: Optional[datetime]
    url_imagem: Optional[str]


class EventUpdateResponse(BaseModel):
    message: str


class EventDeleteResponse(BaseModel):
    message: str


class EventResponse(BaseModel):
    id: int
    id_organizacao: int
    id_usuario: int
    fechado: datetime
    titulo: str
    descricao: str
    data: datetime
    url_imagem: Optional[str] = ''
    criado_em: datetime
    atualizado_em: datetime

    @classmethod
    def from_home(cls, evento):
        url_imagem = evento.url_imagem if evento.url_imagem else ''
        return cls(
            id=evento.id,
            id_organizacao=evento.id_organizacao
            if hasattr(evento, 'id_organizacao')
            else None,
            id_usuario=evento.id_usuario,
            fechado=evento.fechado,
            titulo=evento.titulo,
            descricao=evento.descricao,
            data=evento.data,
            url_imagem=url_imagem,
            criado_em=evento.criado_em,
            atualizado_em=evento.atualizado_em,
        )

    @classmethod
    def from_profile(cls, evento):
        url_imagem = evento.url_imagem if evento.url_imagem else ''
        return cls(
            id=evento.id,
            id_organizacao=evento.id_organizacao,
            id_usuario=evento.id_usuario,
            fechado=evento.fechado,
            titulo=evento.titulo,
            descricao=evento.descricao,
            data=evento.data,
            url_imagem=url_imagem,
            criado_em=evento.criado_em,
            atualizado_em=evento.atualizado_em,
        )
