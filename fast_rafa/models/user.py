# models/user.py

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry
from fast_rafa.schemas.user import CreateUser


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    primeiro_nome: Mapped[str] = mapped_column()
    sobrenome: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    senha_hash: Mapped[str] = mapped_column()
    telefone: Mapped[str] = mapped_column()
    id_organizacao: Mapped[int] = mapped_column(
        Integer, ForeignKey('organizations.id'), nullable=False
    )
    eh_deletado: Mapped[bool] = mapped_column(default=False)
    eh_voluntario: Mapped[bool] = mapped_column(default=False)
    eh_gerente: Mapped[bool] = mapped_column(default=False)
    deficiencia_auditiva: Mapped[Optional[bool]] = mapped_column(default=None)
    usa_cadeira_rodas: Mapped[Optional[bool]] = mapped_column(default=None)
    deficiencia_cognitiva: Mapped[Optional[bool]] = mapped_column(default=None)
    lgbtq: Mapped[Optional[bool]] = mapped_column(default=None)
    url_imagem_perfil: Mapped[Optional[str]] = mapped_column(default=None)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    favorites = relationship(
        'Favorite', back_populates='user', cascade='all, delete-orphan'
    )
    organization = relationship('Organization', back_populates='employees')
    posts = relationship(
        'Post', back_populates='uploader', cascade='all, delete-orphan'
    )
    delivery = relationship(
        'Delivery', back_populates='volunteer', cascade='all, delete-orphan'
    )
    events = relationship(
        'Event', back_populates='manager', cascade='all, delete-orphan'
    )
    watchlist = relationship('Watchlist', back_populates='user')
    sent_messages = relationship(
        'Message', back_populates='sender', cascade='all, delete-orphan'
    )

    def __init__(self, data: CreateUser):  # Tipo Pydantic vindo de schemas
        for key, value in data.dict().items():
            if hasattr(self, key):
                setattr(self, key, value)

    @classmethod
    def create(cls, data: CreateUser):  # Usa o esquema de criação
        return cls(data)

    @classmethod
    def update(cls, instance: 'User', data: dict):
        for key, value in data.items():
            setattr(instance, key, value)
        instance.atualizado_em = datetime.utcnow()
        return instance
