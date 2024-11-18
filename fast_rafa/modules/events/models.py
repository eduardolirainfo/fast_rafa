from datetime import datetime
from typing import Dict, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.modules.base.models import table_registry
from fast_rafa.modules.events.schemas import EventCreate


@table_registry.mapped_as_dataclass
class Event:
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    id_organizacao: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('organizations.id', ondelete='CASCADE'),
        nullable=False,
    )
    id_usuario: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False
    )
    fechado: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    titulo: Mapped[str] = mapped_column(String(50), nullable=False)
    descricao: Mapped[str] = mapped_column(String(255), nullable=False)
    data: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    url_imagem: Mapped[Optional[str]] = mapped_column(
        String(2048), nullable=True
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow()
    )

    __table_args__ = (
        UniqueConstraint(
            'id_organizacao', 'data', name='uix_organizacao_data'
        ),
    )

    organization = relationship('Organization', back_populates='events')
    manager = relationship('User', back_populates='events')

    def __init__(self, data: 'EventCreate'):  # Tipo Pydantic vindo de schemas
        for key, value in data.dict().items():
            if hasattr(self, key):
                setattr(self, key, value)

    @classmethod
    def create(cls, data: 'EventCreate') -> 'Event':
        return cls(data)

    @classmethod
    def update(cls, instance: 'Event', data: Dict):
        """
        Atualiza uma instância existente fornecidos de Event com novos dados.

        :param instance: A instância de Event a ser atualizada.
        :param data: Um dicionário contendo os campos a serem atualizados.
        :raises ValueError: Se a instância for None.
        :return: A instância de Event atualizada.
        """
        if instance is None:
            raise ValueError('A instância não pode ser None')

        for key, value in data.items():
            setattr(instance, key, value)
        instance.atualizado_em = datetime.utcnow()
        return instance

    @classmethod
    def delete(cls, id: int):
        """
        Exclui uma instância de Event com base no ID fornecido.

        :param id: O ID do Event a ser excluído.
        :return: A instância de Event excluída.
        """
        return cls(id=id)
