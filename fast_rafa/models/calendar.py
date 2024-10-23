from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


@table_registry.mapped_as_dataclass
class Calendar():
    __tablename__ = 'calendars'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    id_organizacao: Mapped[int] = mapped_column(
        Integer, ForeignKey('organizations.id'), nullable=False)
    abertura: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    fechamento: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now())

    organizations = relationship('Organization', back_populates='calendars')
