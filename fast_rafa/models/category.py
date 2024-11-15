from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


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

    def to_dict(self) -> Dict[str, Optional[str]]:
        return {
            'id': self.id,
            'categoria': self.categoria,
            'criado_em': self.criado_em.isoformat(),
            'atualizado_em': self.atualizado_em.isoformat()
            if self.atualizado_em
            else None,
        }

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

    class CreateCategory(BaseModel):
        categoria: str

    class CreateCategoryResponse(BaseModel):
        message: str

    class UpdateRequest(BaseModel):
        categoria: str

    class UpdateResponse(BaseModel):
        message: str

    class DeleteResponse(BaseModel):
        message: str
