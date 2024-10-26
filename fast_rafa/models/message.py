from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


@table_registry.mapped_as_dataclass
class Mensagem():
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    id_mensagem_it: Mapped[int] = mapped_column(
        Integer, ForeignKey('message_its.id'), nullable=False)
    id_remetente: Mapped[int] = mapped_column(
        Integer, ForeignKey('users.id'), nullable=False)
    id_postagem: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey('posts.id'), nullable=True)
    conteudo: Mapped[str] = mapped_column(String(500), nullable=False)
    url_imagem: Mapped[Optional[str]] = mapped_column(
        String(2048), nullable=True)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow())
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())

    mensagens = relationship('message_its', back_populates='messages')
    posts = relationship('Post', back_populates='messages')
    remetentes = relationship('User', back_populates='messages')
