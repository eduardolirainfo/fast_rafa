from datetime import datetime
from typing import Dict

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.modules.base.models import table_registry
from fast_rafa.modules.categories.schemas import CreateCategory


@table_registry.mapped_as_dataclass
class Category:
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    categoria: Mapped[str] = mapped_column(
        String(25), nullable=False, unique=True
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(self, data: 'CreateCategory'):
        self.categoria = data.categoria

    posts = relationship('Post', back_populates='categories')

    @classmethod
    def create(cls, data: 'CreateCategory') -> 'Category':
        return cls(data)

    @classmethod
    def update(cls, instance: 'Category', data: Dict):
        for key, value in data.items():
            setattr(instance, key, value)
        return instance

    @classmethod
    def delete(cls, categoria: str):
        return cls(categoria=categoria)
