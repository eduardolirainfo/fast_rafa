from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreatePost(BaseModel):
    item: bool
    id_organizacao: int
    id_usuario: int
    titulo: str
    descricao: str
    quantidade: str
    id_categoria: int
    url_imagem_post: Optional[str] = None
    data_validade: Optional[datetime] = None
    status: Optional[int] = 1


class UpdatePostRequest(BaseModel):
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


class UpdatePostResponse(BaseModel):
    message: str


class DeletePostResponse(BaseModel):
    message: str


class PostResponse(BaseModel):
    id: int
    item: bool
    id_organizacao: int
    id_usuario: int
    titulo: str
    descricao: str
    quantidade: str
    id_categoria: int
    url_imagem_post: Optional[str] = ''
    data_validade: datetime
    status: int
    criado_em: datetime
    atualizado_em: datetime

    @classmethod
    def from_home(cls, post):
        return cls(
            id=post.id,
            item=post.item if hasattr(post, 'item') else False,
            id_organizacao=post.id_organizacao
            if hasattr(post, 'id_organizacao')
            else 0,
            id_usuario=post.id_usuario if hasattr(post, 'id_usuario') else 0,
            titulo=post.titulo if hasattr(post, 'titulo') else '',
            descricao=post.descricao if hasattr(post, 'descricao') else '',
            quantidade=post.quantidade if hasattr(post, 'quantidade') else '',
            id_categoria=post.id_categoria
            if hasattr(post, 'id_categoria')
            else 0,
            url_imagem_post=post.url_imagem_post
            if hasattr(post, 'url_imagem_post')
            else '',
            data_validade=post.data_validade
            if hasattr(post, 'data_validade')
            else datetime.utcnow(),
            status=post.status if hasattr(post, 'status') else 0,
            criado_em=post.criado_em
            if hasattr(post, 'criado_em')
            else datetime.utcnow(),
            atualizado_em=post.atualizado_em
            if hasattr(post, 'atualizado_em')
            else datetime.utcnow(),
        )
