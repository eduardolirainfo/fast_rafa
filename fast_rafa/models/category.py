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

    def __init__(
        self,
        categoria: str,
        criado_em: Optional[datetime] = None,
        atualizado_em: Optional[datetime] = None,
    ):
        self.categoria = categoria
        self.criado_em = criado_em or datetime.utcnow()
        self.atualizado_em = atualizado_em or datetime.utcnow()

    def to_dict(self) -> Dict[str, Optional[str]]:
        return {
            'categoria': self.categoria,
            'criado_em': self.criado_em.isoformat(),
            'atualizado_em': self.atualizado_em.isoformat()
            if self.atualizado_em
            else None,
        }

    posts = relationship('Post', back_populates='categories')

    class Create(BaseModel):
        categoria: str
        criado_em: Optional[datetime] = None
        atualizado_em: Optional[datetime] = None

    @classmethod
    def create(cls, data: Create) -> 'Category':
        return cls(
            categoria=data.categoria,
            criado_em=data.criado_em or datetime.utcnow(),
            atualizado_em=data.atualizado_em or datetime.utcnow(),
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
