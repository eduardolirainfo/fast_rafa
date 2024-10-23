from datetime import datetime

from pydantic import Optional
from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


@table_registry.mapped_as_dataclass
class Watchlist():
    __tablename__ = 'watchlists'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_organizacao: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey('organizations.id'), nullable=True)
    id_usuario: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey('users.id'), nullable=True)
    endereco_ip: Mapped[str] = mapped_column(String, nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    organizacoes = relationship('Organization', back_populates='watchlists')
    usuarios = relationship('User', back_populates='watchlists')
