from datetime import date, datetime
from typing import Dict, Optional

from pydantic import BaseModel
from sqlalchemy import (
    Boolean, Date, DateTime, ForeignKey, Integer, String, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


@table_registry.mapped_as_dataclass
class Post:
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    item: Mapped[bool] = mapped_column(Boolean, nullable=False)
    id_organizacao: Mapped[int] = mapped_column(
        Integer, ForeignKey('organizations.id')
    )
    id_usuario: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    titulo: Mapped[str] = mapped_column(String(25), nullable=False)
    descricao: Mapped[str] = mapped_column(String(120), nullable=False)
    quantidade: Mapped[str] = mapped_column(String(12), nullable=False)
    id_categoria: Mapped[int] = mapped_column(
        Integer, ForeignKey('categories.id')
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
        UniqueConstraint('id_usuario', 'titulo', 'descricao', 'data_validade',
                         name='uix_usuario_titulo_descricao_data'),
    )

    def __init__(self, post_data: 'CreatePostRequest'):
        self.item = post_data.item
        self.id_organizacao = post_data.id_organizacao
        self.id_usuario = post_data.id_usuario
        self.titulo = post_data.titulo
        self.descricao = post_data.descricao
        self.quantidade = post_data.quantidade
        self.id_categoria = post_data.id_categoria
        self.url_imagem_post = post_data.url_imagem_post
        self.data_validade = post_data.data_validade
        self.status = post_data.status
        self.criado_em = post_data.criado_em
        self.atualizado_em = post_data.atualizado_em

    def to_dict(self):
        return {
            'item': self.item,
            'id_organizacao': self.id_organizacao,
            'id_usuario': self.id_usuario,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'quantidade': self.quantidade,
            'id_categoria': self.id_categoria,
            'url_imagem_post': self.url_imagem_post,
            'data_validade': self.data_validade,
            'status': self.status,
            'criado_em': self.criado_em.isoformat(),
            'atualizado_em': self.atualizado_em.isoformat(),
        }

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

    class CreatePostRequest(BaseModel):
        item: bool
        id_organizacao: int
        id_usuario: int
        titulo: str
        descricao: str
        quantidade: str
        id_categoria: int
        url_imagem_post: Optional[str] = None
        data_validade: Optional[datetime] = None
        status: Optional[int] = 1  # 1 = ativo
        criado_em: datetime = datetime.utcnow()
        atualizado_em: datetime = datetime.utcnow()

    @classmethod
    def create(cls, data: CreatePostRequest) -> 'Post':
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

    class UpdateRequest(BaseModel):
        item: Optional[bool]
        id_organizacao: Optional[int]
        id_usuario: Optional[int]
        titulo: Optional[str]
        descricao: Optional[str]
        quantidade: Optional[str]
        id_categoria: Optional[int]
        url_imagem_post: Optional[str]
        data_validade: Optional[datetime]
        status: Optional[int]
        atualizado_em: Optional[datetime] = datetime.utcnow()

    class UpdateResponse(BaseModel):
        message: str

    class DeleteResponse(BaseModel):
        message: str
