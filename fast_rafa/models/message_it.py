from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


@table_registry.mapped_as_dataclass
class MessageIt():
    __tablename__ = 'message_its'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    usuario_um: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id'), nullable=False)
    usuario_dois: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id'), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow())

    mensagens = relationship(
        'Message',
        back_populates='message_its', cascade='all, delete-orphan'
    )
