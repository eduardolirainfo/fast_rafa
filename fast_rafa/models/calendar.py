from datetime import datetime
from typing import Dict

from pydantic import BaseModel
from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


@table_registry.mapped_as_dataclass
class Calendar():
    __tablename__ = 'calendars'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    id_organizacao: Mapped[int] = mapped_column(
        Integer, ForeignKey('organizations.id'), unique=True, nullable=False
    )
    abertura: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow())
    fechamento: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow())
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow())
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow()
    )

    def __init__(
        self, id_organizacao, abertura, fechamento, criado_em=None,
        atualizado_em=None
    ):
        self.id_organizacao = id_organizacao
        self.abertura = abertura
        self.fechamento = fechamento
        self.criado_em = criado_em or datetime.utcnow()
        self.atualizado_em = atualizado_em or datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'id_organizacao': self.id_organizacao,
            'abertura': self.abertura.isoformat(),
            'fechamento': self.fechamento.isoformat(),
            'criado_em': self.criado_em.isoformat(),
            'atualizado_em': self.atualizado_em.isoformat()
        }

    organizations = relationship('Organization', back_populates='calendars')

    class Create(BaseModel):
        id_organizacao: int
        abertura: datetime
        fechamento: datetime
        criado_em: datetime = datetime.utcnow()
        atualizado_em: datetime = datetime.utcnow()

    class UpdateRequest(BaseModel):
        id_organizacao: int
        abertura: datetime
        fechamento: datetime

    class UpdateResponse(BaseModel):
        message: str

    class DeleteResponse(BaseModel):
        message: str

    @classmethod
    def create(cls, data: Create) -> 'Calendar':
        return cls(
            id_organizacao=data.id_organizacao,
            abertura=data.abertura,
            fechamento=data.fechamento,
            criado_em=data.criado_em,
            atualizado_em=data.atualizado_em
        )

    @classmethod
    def update(cls, instance: 'Calendar', data: Dict):
        for key, value in data.items():
            setattr(instance, key, value)
        return instance
