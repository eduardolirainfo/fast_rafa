from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel
from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


@table_registry.mapped_as_dataclass
class Delivery():
    __tablename__ = 'deliveries'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    entrega_direta: Mapped[bool] = mapped_column(Boolean, nullable=False)
    id_postagem: Mapped[int] = mapped_column(
        Integer, ForeignKey('posts.id'), nullable=False, unique=True)
    id_usuario: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id'), nullable=False)
    id_organizacao: Mapped[int] = mapped_column(
        Integer, ForeignKey('organizations.id'), nullable=False)
    id_ong: Mapped[int] = mapped_column(
        Integer, ForeignKey('organizations.id'), nullable=False)
    data: Mapped[datetime] = mapped_column(Date, nullable=False)
    hora: Mapped[str] = mapped_column(String, nullable=False)
    completo: Mapped[int] = mapped_column(Integer, nullable=False)
    motivo_cancelamento: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow())
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    posts = relationship('Post', back_populates='deliveries', uselist=False)
    users = relationship('User', back_populates='deliveries')

    organizations = relationship(
        'Organization',
        back_populates='deliveries_as_org',
        foreign_keys=[id_organizacao]
        )

    ongs = relationship(
        'Organization',
        back_populates='deliveries_as_ong',
        foreign_keys=[id_ong]
    )

    def __init__(self, entrega_direta: bool,
                 id_postagem: int, id_usuario: int, id_organizacao: int,
                 id_ong: int, data: datetime, hora: str, completo: int,
                 motivo_cancelamento: Optional[str],
                 criado_em=None, atualizado_em=None):
        self.entrega_direta = entrega_direta
        self.id_postagem = id_postagem
        self.id_usuario = id_usuario
        self.id_organizacao = id_organizacao
        self.id_ong = id_ong
        self.data = data
        self.hora = hora
        self.completo = completo
        self.motivo_cancelamento = motivo_cancelamento
        self.criado_em = criado_em
        self.atualizado_em = atualizado_em

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "entrega_direta": self.entrega_direta,
            "id_postagem": self.id_postagem,
            "id_usuario": self.id_usuario,
            "id_organizacao": self.id_organizacao,
            "id_ong": self.id_ong,
            "data": self.data.isoformat(),
            "hora": self.hora,
            "completo": self.completo,
            "motivo_cancelamento": self.motivo_cancelamento,
            "criado_em": self.criado_em.isoformat(),
            "atualizado_em": self.atualizado_em.isoformat()
            if self.atualizado_em else None
        }

    class Create(BaseModel):
        entrega_direta: bool
        id_postagem: int
        id_usuario: int
        id_organizacao: int
        id_ong: int
        data: datetime = datetime.utcnow()
        hora: str
        completo: int
        motivo_cancelamento: Optional[str]
        criado_em: datetime = datetime.utcnow()
        atualiza_em: datetime = datetime.utcnow()

    @classmethod
    def create(cls, data: Create) -> 'Delivery':
        return cls(
            entrega_direta=data.entrega_direta,
            id_postagem=data.id_postagem,
            id_usuario=data.id_usuario,
            id_organizacao=data.id_organizacao,
            id_ong=data.id_ong,
            data=data.data,
            hora=data.hora,
            completo=data.completo,
            motivo_cancelamento=data.motivo_cancelamento,
            criado_em=data.criado_em,
            atualizado_em=data.atualiza_em
        )

    @classmethod
    def update(cls, instance: 'Delivery', data: Dict):
        for key, value in data.items():
            setattr(instance, key, value)
        return instance

    @classmethod
    def delete(cls, id: int):
        return cls(id=id)

    class UpdateRequest(BaseModel):
        entrega_direta: bool
        id_postagem: int
        id_usuario: int
        id_organizacao: int
        id_ong: int
        data: datetime
        hora: str
        completo: int
        motivo_cancelamento: Optional[str]
        atualizado_em: datetime = datetime.utcnow()

    class UpdateResponse(BaseModel):
        message: str

    class DeleteRequest(BaseModel):
        message: str
