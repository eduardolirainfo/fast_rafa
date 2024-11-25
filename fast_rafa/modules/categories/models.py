from datetime import datetime
from typing import Dict

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.modules.base.models import table_registry
from fast_rafa.modules.categories.schemas import CreateCategory


@table_registry.mapped_as_dataclass
class Category:
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    id_categoria_principal: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('categories_main.id', ondelete='CASCADE'),
        nullable=False,  # Campo obrigatório
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

    # Relacionamentos
    posts = relationship('Post', back_populates='categories')
    categoriesMain = relationship('CategoryMain', back_populates='categories')

    def __init__(self, data: 'CreateCategory'):
        """Inicializa a categoria com base no schema recebido."""
        self.categoria = data.categoria
        self.id_categoria_principal = data.id_categoria_principal
        self.slug = data.slug
        self.icon = data.icon

    @classmethod
    def create(cls, data: 'CreateCategory') -> 'Category':
        """Método de criação da categoria."""
        return cls(data)

    @classmethod
    def update(cls, instance: 'Category', data: Dict) -> 'Category':
        """Método para atualizar uma instância de categoria com novos dados."""
        for key, value in data.items():
            setattr(instance, key, value)
        return instance

    @classmethod
    def delete(cls, categoria: str) -> 'Category':
        """Método para excluir uma categoria (por nome)."""
        return cls(categoria=categoria)
