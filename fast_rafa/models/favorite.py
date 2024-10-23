from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


@table_registry.mapped_as_dataclass
class Favorite:
    __tablename__ = 'favorites'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    id_postagem: Mapped[int] = mapped_column(Integer, ForeignKey('posts.id'))
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))

    posts = relationship('Post', back_populates='favorites')
    users = relationship('User', back_populates='favorites')

    @classmethod
    def create(cls, data: dict):
        favorite = cls(**data)
        return favorite

    @classmethod
    def update(cls, data: dict):
        favorite = cls(**data)
        return favorite

    @classmethod
    def delete(cls, data: dict):
        favorite = cls(**data)
        return favorite

    @classmethod
    def read_by_name(cls, name: str):
        favorite = cls.query.filter_by(name=name).first().upper()
        return favorite

    @classmethod
    def read_by_id(cls, id: int):
        favorite = cls.query.get(id)
        return favorite
