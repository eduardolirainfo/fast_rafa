from datetime import date, datetime
from typing import Dict, Optional

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.modules.base.models import table_registry
from fast_rafa.modules.posts.schemas import CreatePost


@table_registry.mapped_as_dataclass
class Post:
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    item: Mapped[bool] = mapped_column(Boolean, nullable=False)
    id_organizacao: Mapped[int] = mapped_column(
        Integer, ForeignKey('organizations.id', ondelete='CASCADE')
    )
    id_usuario: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id', ondelete='CASCADE')
    )
    titulo: Mapped[str] = mapped_column(String(25), nullable=False)
    descricao: Mapped[str] = mapped_column(String(120), nullable=False)
    quantidade: Mapped[str] = mapped_column(String(12), nullable=False)
    id_categoria: Mapped[int] = mapped_column(
        Integer, ForeignKey('categories.id', ondelete='CASCADE')
    )
    url_imagem_post: Mapped[Optional[str]] = mapped_column(
        String(2048), nullable=True
    )
    data_validade: Mapped[date] = mapped_column(
        Date, nullable=False, default=lambda: datetime.utcnow().date()
    )
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow()
    )

    __table_args__ = (
        UniqueConstraint(
            'id_usuario',
            'titulo',
            'descricao',
            'data_validade',
            name='uix_usuario_titulo_descricao_data',
        ),
    )

    def __init__(self, data: 'CreatePost'):
        for key, value in data.dict().items():
            if hasattr(self, key):
                setattr(self, key, value)

    organizations = relationship('Organization', back_populates='posts')
    uploader = relationship('User', back_populates='posts')
    categories = relationship(
        'Category', foreign_keys=[id_categoria], back_populates='posts'
    )
    delivery = relationship(
        'Delivery', back_populates='post', cascade='all, delete-orphan'
    )
    favorites = relationship(
        'Favorite', back_populates='posts', cascade='all, delete-orphan'
    )
    message = relationship('Message', back_populates='post')

    @classmethod
    def create(cls, data: 'CreatePost') -> 'Post':
        return cls(data)

    @classmethod
    def update(cls, instance: 'Post', data: Dict):
        for key, value in data.items():
            setattr(instance, key, value)
        instance.atualizado_em = datetime.utcnow()
        return instance

    @classmethod
    def delete(cls, data: dict):
        post = cls(**data)
        return post
