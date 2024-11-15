from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


@table_registry.mapped_as_dataclass
class Message:
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    id_mensagem_it: Mapped[int] = mapped_column(
        Integer, ForeignKey('message_its.id'), nullable=False
    )
    id_remetente: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id'), nullable=False
    )
    id_postagem: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey('posts.id'), nullable=True
    )
    conteudo: Mapped[str] = mapped_column(String(500), nullable=False)
    url_imagem: Mapped[Optional[str]] = mapped_column(
        String(2048), nullable=True
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow()
    )

    message_it = relationship('MessageItem', back_populates='messages')
    post = relationship('Post', back_populates='message')
    sender = relationship('User', back_populates='sent_messages')

    def __init__(
        self,
        id_mensagem_it: int,
        id_remetente: int,
        id_postagem: Optional[int],
        conteudo: str,
        url_imagem: Optional[str],
    ):
        self.id_mensagem_it = id_mensagem_it
        self.id_remetente = id_remetente
        self.id_postagem = id_postagem
        self.conteudo = conteudo
        self.url_imagem = url_imagem

    def to_dict(self) -> dict:
        return {
            'id_mensagem_it': self.id_mensagem_it,
            'id_remetente': self.id_remetente,
            'id_postagem': self.id_postagem,
            'conteudo': self.conteudo,
            'url_imagem': self.url_imagem,
            'criado_em': self.criado_em,
            'atualizado_em': self.atualizado_em,
        }

    @classmethod
    def create(cls, data: 'CreateMessage') -> 'Message':
        return cls(
            id_mensagem_it=data.id_mensagem_it,
            id_remetente=data.id_remetente,
            id_postagem=data.id_postagem,
            conteudo=data.conteudo,
            url_imagem=data.url_imagem,
        )

    @classmethod
    def update(cls, instance: 'Message', data: Dict):
        """Atualiza uma instância de Mensagem com base nos dados fornecidos.
        Args:
            instance (Message): Instância de Mensagem a ser atualizada.
            data (Dict): Dados para atualizar a instância de Mensagem.
        """
        if instance is None:
            raise ValueError('A instância não pode ser None')

        for key, value in data.items():
            setattr(instance, key, value)
        instance.atualizado_em = datetime.utcnow()
        return instance

    @classmethod
    def delete(cls, id: int):
        """Deleta uma instância de Mensagem com base no ID fornecido.
        Args:
            id (int): ID da Mensagem a ser deletada.
        """
        return cls(id=id)

    class CreateMessage(BaseModel):
        id_mensagem_it: int
        id_remetente: int
        id_postagem: Optional[int]
        conteudo: str
        url_imagem: Optional[str]

    class UpdateRequest(BaseModel):
        id_mensagem_it: Optional[int]
        id_remetente: Optional[int]
        id_postagem: Optional[int]
        conteudo: Optional[str]
        url_imagem: Optional[str]

    class UpdateResponse(BaseModel):
        message: str

    class DeleteResponse(BaseModel):
        message: str
