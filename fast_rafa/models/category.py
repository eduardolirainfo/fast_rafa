from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel
from sqlalchemy import Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


@table_registry.mapped_as_dataclass
class Category:
    __tablename__ = 'categories'

    id: Mapped[Optional[int]] = mapped_column(Integer, primary_key=True)
    categoria: Mapped[str] = mapped_column(String(25), nullable=False)
    criado_em: Mapped[datetime] = mapped_column(default=func.now())
    atualizado_em: Mapped[Optional[datetime]] = mapped_column(
        default=func.now(), onupdate=func.now()
    )

    posts = relationship('Post', back_populates='categories')

    def __init__(self, categoria: str, id: Optional[int] = None):
        self.categoria = categoria
        self.id = id

    def to_dict(self) -> Dict[str, Optional[str]]:
        return {
            "id": self.id,
            "categoria": self.categoria,
            "criado_em": self.criado_em.isoformat(),
            "atualizado_em": self.atualizado_em.isoformat()
            if self.atualizado_em else None
        }

    @classmethod
    def create(cls, categoria: str):
        return cls(categoria=categoria)

    # Atualização para receber apenas a categoria
    @classmethod
    def update(cls, instance: "Category", categoria: str):
        instance.categoria = categoria
        instance.atualizado_em = datetime.now()  # Atualiza o timestamp
        return instance

    @classmethod
    def delete(cls, categoria: str):
        return cls(categoria=categoria)

    @classmethod
    def read_by_name(cls, categoria: str):
        return categoria.strip().upper()

    @classmethod
    def read_by_id(cls, category_id: int):
        return cls(id=category_id, categoria="")

    class UpdateRequest(BaseModel):
        categoria: str

    class UpdateResponse(BaseModel):
        message: str

    class DeleteResponse(BaseModel):
        message: str
