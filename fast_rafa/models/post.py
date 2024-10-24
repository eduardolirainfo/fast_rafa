from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


@table_registry.mapped_as_dataclass
class Post:
    __tablename__ = 'posts'

    id: Mapped[Optional[int]] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
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
    url_imagem_post: Mapped[Optional[str]] = mapped_column(default=None)
    data_validade: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=func.now())
    status: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now())
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=datetime.now()
    )

    def __init__(
        self, item, id_organizacao, id_usuario, titulo, descricao, quantidade,
        id_categoria,
        url_imagem_post=None, data_validade=None, status=None, criado_em=None,
        atualizado_em=None
    ):
        self.item = item
        self.id_organizacao = id_organizacao
        self.id_usuario = id_usuario
        self.titulo = titulo
        self.descricao = descricao
        self.quantidade = quantidade
        self.id_categoria = id_categoria
        self.url_imagem_post = url_imagem_post
        self.data_validade = data_validade
        self.status = status
        self.criado_em = criado_em
        self.atualizado_em = atualizado_em

    def to_dict(self):
        return {
            'id': self.id,
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
            'criado_em': self.criado_em,
            'atualizado_em': self.atualizado_em
        }

    organizations = relationship('Organization', back_populates='posts')
    users = relationship('User', back_populates='posts')
    categories = relationship('Category', back_populates='posts')
    deliveries = relationship('Delivery', back_populates='posts')
    favorites = relationship('Favorite', back_populates='posts')

    class Create(BaseModel):
        item: bool
        id_organizacao: int
        id_usuario: int
        titulo: str
        descricao: str
        quantidade: str
        id_categoria: int
        url_imagem_post: Optional[str]
        data_validade: Optional[datetime]
        status: Optional[int]
        criado_em: datetime = datetime.utcnow()
        atualizado_em: datetime = datetime.utcnow()

    @classmethod
    def create(cls, data: Create) -> 'Post':
        return cls(
            item=data.item,
            id_organizacao=data.id_organizacao,
            id_usuario=data.id_usuario,
            titulo=data.titulo,
            descricao=data.descricao,
            quantidade=data.quantidade,
            id_categoria=data.id_categoria,
            url_imagem_post=data.url_imagem_post,
            data_validade=data.data_validade,
            status=data.status,
            criado_em=data.criado_em,
            atualizado_em=data.atualizado_em
        )

    @classmethod
    def update(cls, data: dict):
        post = cls(**data)
        return post

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

    class UpdateResponse(BaseModel):
        message: str

    class DeleteResponse(BaseModel):
        message: str
