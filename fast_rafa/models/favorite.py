from typing import Optional

from pydantic import BaseModel
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


@table_registry.mapped_as_dataclass
class Favorite:
    __tablename__ = 'favorites'

    id: Mapped[Optional[int]] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    id_postagem: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'))
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    def __init__(self, id_postagem: int, id_usuario: int):
        self.id_postagem = id_postagem
        self.id_usuario = id_usuario

    def to_dict(self):
        return {
            'id': self.id,
            'id_postagem': self.id_postagem,
            'id_usuario': self.id_usuario,
        }

    class Create(BaseModel):
        id_postagem: int
        id_usuario: int

    posts = relationship('Post', back_populates='favorites')
    users = relationship('User', back_populates='favorites')

    @classmethod
    def create(cls, data: Create):
        favorite = cls(**data.dict())
        return favorite

    @classmethod
    def update(cls, data: dict):
        favorite = cls(**data)
        return favorite

    @classmethod
    def delete(cls, data: dict):
        favorite = cls(**data)
        return favorite

    class UpdateRequest(BaseModel):
        id_postagem: Optional[int]
        id_usuario: Optional[int]

    class UpdateResponse(BaseModel):
        message: str

    class DeleteResponse(BaseModel):
        message: str
