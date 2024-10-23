from datetime import datetime
from typing import Optional

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
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    data: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    url_imagem: Mapped[Optional[str]] = mapped_column(
        String(2048), nullable=True)
    createdAt: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updatedAt: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now())

    organizations = relationship('Organization', back_populates='events')
    gerentes = relationship('User', back_populates='events')
