from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel
from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


@table_registry.mapped_as_dataclass
class Category:
    __tablename__ = 'categories'

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    categoria: Mapped[str] = mapped_column(
        String(25), nullable=False, unique=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now())
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=datetime.now()
    )

    def __init__(self, categoria: str,
                 id: Optional[int] = None,
                 criado_em=None, atualizado_em=None):
        self.categoria = categoria
        self.id = id
        self.criado_em = criado_em
        self.atualizado_em = atualizado_em

    def to_dict(self) -> Dict[str, Optional[str]]:
        return {
            "id": self.id,
            "categoria": self.categoria,
            "criado_em": self.criado_em.isoformat(),
            "atualizado_em": self.atualizado_em.isoformat()
            if self.atualizado_em else None
        }

    posts = relationship('Post', back_populates='categories')

    class Create(BaseModel):
        categoria: str
        created_at: datetime = datetime.now()
        updated_at: datetime = datetime.now()

    @classmethod
    def create(cls, data: Create) -> 'Category':
        return cls(
            categoria=data.categoria,
            criado_em=data.created_at,
            atualizado_em=data.updated_at
        )

    @classmethod
    def update(cls, instance: 'Category', data: Dict):
        for key, value in data.items():
            setattr(instance, key, value)
        return instance

    @classmethod
    def delete(cls, categoria: str):
        return cls(categoria=categoria)

    class UpdateRequest(BaseModel):
        categoria: str

    class UpdateResponse(BaseModel):
        message: str

    class DeleteResponse(BaseModel):
        message: str
