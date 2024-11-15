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


class PostRead(BaseModel):
    item: bool
    id_organizacao: int
    id_usuario: int
    titulo: str
    descricao: str
    quantidade: str
    id_categoria: int
    url_imagem_post: Optional[str] = None
    data_validade: datetime
    status: int
    criado_em: datetime
    atualizado_em: datetime

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

    class Config:
        from_attributes = True
