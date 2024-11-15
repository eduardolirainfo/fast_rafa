from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel
from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


@table_registry.mapped_as_dataclass
class Favorite:
    __tablename__ = 'favorites'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    id_postagem: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'))
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow()
    )

    def __init__(
        self,
        id_postagem: int,
        id_usuario: int,
        criado_em: Optional[datetime] = None,
    ):
        self.id_postagem = id_postagem
        self.id_usuario = id_usuario
        self.criado_em = criado_em or datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'id_postagem': self.id_postagem,
            'id_usuario': self.id_usuario,
            'criado_em': self.criado_em.isoformat(),
        }

    class CreateFavorite(BaseModel):
        id_postagem: int
        id_usuario: int
        criado_em: datetime = datetime.utcnow()

    posts = relationship('Post', back_populates='favorites')
    user = relationship('User', back_populates='favorites')

    @classmethod
    def create(cls, data: CreateFavorite) -> 'Favorite':
        return cls(
            id_postagem=data.id_postagem,
            id_usuario=data.id_usuario,
            criado_em=data.criado_em,
        )

    @classmethod
    def update(cls, instance: 'Favorite', data: Dict):
        for key, value in data.items():
            setattr(instance, key, value)
        return instance

    @classmethod
    def delete(cls, data: dict):
        favorite = cls(**data)
        return favorite

    class UpdateRequestFavorite(BaseModel):
        id_postagem: Optional[int]
        id_usuario: Optional[int]

    class UpdateResponseFavorite(BaseModel):
        message: str

        def to_dict(self):
            return {'message': self.message}

    class DeleteResponseFavorite(BaseModel):
        message: str

        def to_dict(self):
            return {'message': self.message}
