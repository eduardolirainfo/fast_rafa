from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.modules.base.models import table_registry


@table_registry.mapped_as_dataclass
class Watchlist:
    __tablename__ = 'watchlists'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    id_organizacao: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('organizations.id', ondelete='CASCADE'),
        nullable=True,
    )
    id_usuario: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True
    )
    endereco_ip: Mapped[str] = mapped_column(String, nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow()
    )

    def __init__(
        self,
        id_organizacao: Optional[int] = None,
        id_usuario: Optional[int] = None,
        endereco_ip: str = '',
        quantidade: int = 0,
    ):
        self.id_organizacao = id_organizacao
        self.id_usuario = id_usuario
        self.endereco_ip = endereco_ip
        self.quantidade = quantidade

    def to_dict(self):
        return {
            'id': self.id,
            'id_organizacao': self.id_organizacao,
            'id_usuario': self.id_usuario,
            'endereco_ip': self.endereco_ip,
            'quantidade': self.quantidade,
            'criado_em': self.criado_em.isoformat(),
        }

    class Create(BaseModel):
        id_organizacao: int
        id_usuario: int
        endereco_ip: str
        quantidade: int
        criado_em: datetime = datetime.utcnow()

    @classmethod
    def create(cls, data: Create) -> 'Watchlist':
        return cls(
            id_organizacao=data.id_organizacao,
            id_usuario=data.id_usuario,
            endereco_ip=data.endereco_ip,
            quantidade=data.quantidade,
            criado_em=data.criado_em,
        )

    @classmethod
    def update(cls, instance: 'Watchlist', data: Dict):
        for key, value in data.items():
            setattr(instance, key, value)
        return instance

    @classmethod
    def delete(cls, data: dict):
        watchlist = cls(**data)
        return watchlist

    organizations = relationship('Organization', back_populates='watchlists')
    user = relationship('User', back_populates='watchlist')

    class UpdateRequest(BaseModel):
        id_organizacao: Optional[int]
        id_usuario: Optional[int]
        endereco_ip: Optional[str]
        quantidade: Optional[int]

    class UpdateResponse(BaseModel):
        message: str

    class DeleteResponse(BaseModel):
        message: str
