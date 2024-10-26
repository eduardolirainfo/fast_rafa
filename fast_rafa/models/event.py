from datetime import datetime
from typing import Dict, Optional
from pydantic import BaseModel
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


@table_registry.mapped_as_dataclass
class Event():
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    id_organizacao: Mapped[int] = mapped_column(
        Integer, ForeignKey('organizations.id'), nullable=False)
    id_usuario: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id'), nullable=False)
    fechado: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    titulo: Mapped[str] = mapped_column(String(50), nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=False)
    data: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    url_imagem: Mapped[Optional[str]] = mapped_column(
        String(2048), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow())
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow()
    )

    organizations = relationship('Organization', back_populates='events')
    gerentes = relationship('User', back_populates='events',
                            foreign_keys=[id_usuario])


    def __init__(self, id_organizacao: int, id_usuario: int, fechado: datetime,
                 titulo: str, descricao: str, data: datetime,
                 url_imagem: Optional[str],
                 criado_em=None, atualizado_em=None):
        self.id_organizacao = id_organizacao
        self.id_usuario = id_usuario
        self.fechado = fechado
        self.titulo = titulo
        self.descricao = descricao
        self.data = data
        self.url_imagem = url_imagem
        self.criado_em = criado_em
        self.atualizado_em = atualizado_em

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'id_organizacao': self.id_organizacao,
            'id_usuario': self.id_usuario,
            'fechado': self.fechado,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'data': self.data,
            'url_imagem': self.url_imagem,
            'criado_em': self.criado_em,
            'atualizado_em': self.atualizado_em
        }

    class Create(BaseModel):
        id_organizacao: int
        id_usuario: int
        fechado: datetime
        titulo: str
        descricao: str
        data: datetime
        url_imagem: Optional[str]

    @classmethod
    def create(cls, data: Create) -> 'Event':
        return cls(
            id_organizacao=data.id_organizacao,
            id_usuario=data.id_usuario,
            fechado=data.fechado,
            titulo=data.titulo,
            descricao=data.descricao,
            data=data.data,
            url_imagem=data.url_imagem,
            criado_em=data.criado_em,
            atualizado_em=data.atualizado_em
        )

    @classmethod
    def update(cls, instance: 'Event', data: Dict):
        for key, value in data.items():
            setattr(instance, key, value)
        return instance

    @classmethod
    def delete(cls, id: int):
        return cls(id=id)

    class UpdateRequest(BaseModel):
        id_organizacao: Optional[int]
        id_usuario: Optional[int]
        fechado: Optional[datetime]
        titulo: Optional[str]
        descricao: Optional[str]
        data: Optional[datetime]
        url_imagem: Optional[str]
        atualizado_em: datetime = datetime.utcnow()

    class UpdateResponse(BaseModel):
        message: str

    class DeleteResponse(BaseModel):
        message: str
