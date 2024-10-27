from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel
from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


@table_registry.mapped_as_dataclass
class MessageItem:
    __tablename__ = 'message_its'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    usuario_um: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id'), nullable=False
    )
    usuario_dois: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id'), nullable=False
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow()
    )

    messages = relationship(
        'Message', back_populates='message_it', cascade='all, delete-orphan'
    )

    def __init__(self, usuario_um: int, usuario_dois: int):
        self.usuario_um = usuario_um
        self.usuario_dois = usuario_dois

    def to_dict(self) -> dict:
        return {
            'usuario_um': self.usuario_um,
            'usuario_dois': self.usuario_dois,
            'messages': {
                message.id: message.to_dict() for message in self.messages
            },
            'criado_em': self.criado_em,
        }

    class CreateMessageItem(BaseModel):
        usuario_um: int
        usuario_dois: int
        criado_em: datetime = datetime.utcnow()

    @classmethod
    def create(cls, data: CreateMessageItem) -> 'MessageItem':
        return cls(
            usuario_um=data.usuario_um,
            usuario_dois=data.usuario_dois,
            criado_em=data.criado_em,
        )

    @classmethod
    def update(cls, instance: 'MessageItem', data: Dict):
        for key, value in data.items():
            setattr(instance, key, value)
        return instance

    @classmethod
    def delete(cls, id: int):
        return cls(id=id)

    class UpdateRequest(BaseModel):
        usuario_um: Optional[int]
        usuario_dois: Optional[int]
        criado_em: Optional[datetime]

    class UpdateResponse(BaseModel):
        message: str

    class DeleteResponse(BaseModel):
        message: str
