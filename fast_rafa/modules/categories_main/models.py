from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.modules.base.models import table_registry
from fast_rafa.modules.categories_main.schemas import (
    CategoryMainCreate,
)


@table_registry.mapped_as_dataclass
class CategoryMain:
    __tablename__ = 'categories_main'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    categoria: Mapped[str] = mapped_column(
        String(25), nullable=False, unique=True
    )
    slug: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    icon: Mapped[str] = mapped_column(String(255), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    categories = relationship('Category', back_populates='categoriesMain')

    def __init__(self, data: 'CategoryMainCreate'):
        self.categoria = data.categoria
        self.slug = data.slug
        self.icon = data.icon

    @classmethod
    def create(cls, data: 'CategoryMainCreate') -> 'CategoryMain':
        return cls(data)
