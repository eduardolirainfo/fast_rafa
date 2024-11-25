# models/user.py

import enum
from datetime import date, datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.modules.base.models import table_registry
from fast_rafa.modules.users.schemas import CreateUser


class SexoEnum(str, enum.Enum):
    MASCULINO = 'M'
    FEMININO = 'F'
    OUTRO = 'O'
    NAO_INFORMADO = 'NI'


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    primeiro_nome: Mapped[str] = mapped_column(String(100))
    sobrenome: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    username: Mapped[str] = mapped_column(String(150), unique=True)
    senha_hash: Mapped[str] = mapped_column(String(60), nullable=False)
    telefone: Mapped[str] = mapped_column(String(20), nullable=False)
    id_organizacao: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('organizations.id', ondelete='CASCADE'),
        nullable=False,
    )
    url_imagem_perfil: Mapped[Optional[String]] = mapped_column(
        String, nullable=True
    )
    eh_deletado: Mapped[bool] = mapped_column(Boolean, default=False)
    eh_voluntario: Mapped[bool] = mapped_column(Boolean, default=False)
    eh_gerente: Mapped[bool] = mapped_column(Boolean, default=False)
    deficiencia_auditiva: Mapped[Optional[bool]] = mapped_column(
        Boolean, default=None
    )
    usa_cadeira_rodas: Mapped[Optional[bool]] = mapped_column(
        Boolean, default=None
    )
    deficiencia_cognitiva: Mapped[Optional[bool]] = mapped_column(
        Boolean, default=None
    )
    lgbtq: Mapped[Optional[bool]] = mapped_column(Boolean, default=None)
    aniversario: Mapped[Optional[date]] = mapped_column(Date, default=None)
    sexo: Mapped[Optional[SexoEnum]] = mapped_column(
        Enum(SexoEnum), default=None
    )
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

    @property
    def get_user_with_organization(self):
        """Propriedade que retorna o usuário com a organização carregada"""
        if self.organization:
            return self
        return None
