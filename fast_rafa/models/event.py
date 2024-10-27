from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel
from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


@table_registry.mapped_as_dataclass
class Event:
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    id_organizacao: Mapped[int] = mapped_column(
        Integer, ForeignKey('organizations.id'), nullable=False
    )
    id_usuario: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id'), nullable=False
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
            'atualizado_em': self.atualizado_em,
        }

    @classmethod
    def create(cls, data: 'CreateEvent') -> 'Event':
        return cls(**data.dict())

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

    class CreateEvent(BaseModel):
        id_organizacao: int
        id_usuario: int
        fechado: datetime
        titulo: str
        descricao: str
        data: datetime
        url_imagem: Optional[str]

    class UpdateRequestEvent(BaseModel):
        id_organizacao: Optional[int]
        id_usuario: Optional[int]
        fechado: Optional[datetime]
        titulo: Optional[str]
        descricao: Optional[str]
        data: Optional[datetime]
        url_imagem: Optional[str]

    class UpdateResponseEvent(BaseModel):
        message: str

        def to_dict(self):
            return {'message': self.message}

    class DeleteResponseEvent(BaseModel):
        message: str

        def to_dict(self):
            return {'message': self.message}
