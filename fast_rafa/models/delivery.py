from datetime import datetime
from typing import Optional

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
    entregue: Mapped[bool] = mapped_column(Boolean, nullable=False)
    id_postagem: Mapped[int] = mapped_column(
        Integer, ForeignKey('posts.id'), nullable=False)
    id_usuario: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id'), nullable=False)
    id_organizacao: Mapped[int] = mapped_column(
        Integer, ForeignKey('organizations.id'), nullable=False)
    id_ong: Mapped[int] = mapped_column(
        Integer, nullable=True)
    data: Mapped[datetime] = mapped_column(Date, nullable=False)
    hora: Mapped[str] = mapped_column(String, nullable=False)
    completo: Mapped[int] = mapped_column(Integer, nullable=False)
    motivo_cancelamento: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=func.now())
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now())

    posts = relationship('Post', back_populates='deliveries', uselist=False)
    users = relationship('User', back_populates='deliveries')
    organizations = relationship("Organization", back_populates="deliveries")
