from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


@table_registry.mapped_as_dataclass
class Post:
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    item: Mapped[bool] = mapped_column(Boolean, nullable=False)
    id_organizacao: Mapped[int] = mapped_column(
        Integer, ForeignKey('organizations.id')
    )
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    titulo: Mapped[str] = mapped_column(String(25), nullable=False)
    descricao: Mapped[str] = mapped_column(String(120), nullable=False)
    quantidade: Mapped[str] = mapped_column(String(12), nullable=False)
    id_categoria: Mapped[int] = mapped_column(
        Integer, ForeignKey('categories.id')
    )
    url_imagem_post: Mapped[Optional[str]] = mapped_column(default=None)
    data_validade: Mapped[datetime] = mapped_column(
        Date, nullable=False, default=func.now())
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    criado_em: Mapped[datetime] = mapped_column(default=func.now())
    atualizado_em: Mapped[Optional[datetime]] = mapped_column(
        default=func.now()
    )

    organizations = relationship('Organization', back_populates='posts')
    users = relationship('User', back_populates='posts')
    categories = relationship('Category', back_populates='posts')
    deliveries = relationship('Delivery', back_populates='posts')
    favorites = relationship('Favorite', back_populates='posts')
