from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, constr
from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    primeiro_nome: Mapped[constr(max_length=50)]
    sobrenome: Mapped[constr(max_length=50)]
    email: Mapped[str] = mapped_column(unique=True)
    senha_hash: Mapped[constr(max_length=255)]
    telefone: Mapped[constr(max_length=20)]
    id_organizacao: Mapped[int] = mapped_column(
        Integer, ForeignKey('organizations.id'), nullable=False
    )
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

    class CreateUserRequest(BaseModel):
        primeiro_nome: constr(max_length=50)
        sobrenome: constr(max_length=50)
        email: str
        senha_hash: constr(max_length=255)
        telefone: constr(max_length=20)
        id_organizacao: Optional[int] = None
        eh_voluntario: bool = False
        eh_gerente: bool = False
        deficiencia_auditiva: Optional[bool] = None
        usa_cadeira_rodas: Optional[bool] = None
        deficiencia_cognitiva: Optional[bool] = None
        lgbtq: Optional[bool] = None
        url_imagem_perfil: Optional[str] = None

    def __init__(self, user_data: CreateUserRequest):
        self.primeiro_nome = user_data.primeiro_nome
        self.sobrenome = user_data.sobrenome
        self.email = user_data.email
        self.senha_hash = user_data.senha_hash
        self.telefone = user_data.telefone
        self.id_organizacao = user_data.id_organizacao
        self.eh_voluntario = user_data.eh_voluntario
        self.eh_gerente = user_data.eh_gerente
        self.deficiencia_auditiva = user_data.deficiencia_auditiva
        self.usa_cadeira_rodas = user_data.usa_cadeira_rodas
        self.deficiencia_cognitiva = user_data.deficiencia_cognitiva
        self.lgbtq = user_data.lgbtq
        self.url_imagem_perfil = user_data.url_imagem_perfil

    def to_dict(self):
        return {
            'id': self.id,
            'id_organizacao': self.id_organizacao,
            'eh_voluntario': self.eh_voluntario,
            'eh_gerente': self.eh_gerente,
            'primeiro_nome': self.primeiro_nome,
            'sobrenome': self.sobrenome,
            'email': self.email,
            'telefone': self.telefone,
            'url_imagem_perfil': self.url_imagem_perfil,
            'criado_em': self.criado_em,
        }

    def home_dict(self):
        return {
            'id': self.id,
            'id_organizacao': self.id_organizacao,
            'primeiro_nome': self.primeiro_nome,
            'sobrenome': self.sobrenome,
            'url_imagem_perfil': self.url_imagem_perfil,
        }

    def profile_dict(self):
        return {
            'id': self.id,
            'id_organizacao': self.id_organizacao,
            'eh_voluntario': self.eh_voluntario,
            'eh_gerente': self.eh_gerente,
            'primeiro_nome': self.primeiro_nome,
            'sobrenome': self.sobrenome,
            'email': self.email,
            'telefone': self.telefone,
            'url_imagem_perfil': self.url_imagem_perfil,
            'favorites': {
                favorite.id_postagem: favorite.to_dict()
                for favorite in self.favorites
            },
            'criado_em': self.criado_em,
        }

    class Create(BaseModel):
        primeiro_nome: constr(max_length=50)
        sobrenome: constr(max_length=50)
        email: str
        senha_hash: constr(max_length=255)
        telefone: constr(max_length=20)
        id_organizacao: Optional[int] = None
        eh_voluntario: bool = False
        eh_gerente: bool = False
        deficiencia_auditiva: Optional[bool] = None
        usa_cadeira_rodas: Optional[bool] = None
        deficiencia_cognitiva: Optional[bool] = None
        lgbtq: Optional[bool] = None
        url_imagem_perfil: Optional[str] = None

    @classmethod
    def create(cls, data: Create) -> 'User':
        return cls(
            primeiro_nome=data.primeiro_nome,
            sobrenome=data.sobrenome,
            email=data.email,
            senha_hash=data.senha_hash,
            telefone=data.telefone,
            id_organizacao=data.id_organizacao,
            eh_voluntario=data.eh_voluntario,
            eh_gerente=data.eh_gerente,
            deficiencia_auditiva=data.deficiencia_auditiva,
            usa_cadeira_rodas=data.usa_cadeira_rodas,
            deficiencia_cognitiva=data.deficiencia_cognitiva,
            lgbtq=data.lgbtq,
            url_imagem_perfil=data.url_imagem_perfil,
        )

    @classmethod
    def update(cls, instance: 'User', data: Dict):
        for key, value in data.items():
            setattr(instance, key, value)
        instance.atualizado_em = datetime.utcnow()
        return instance

    class UpdateRequest(BaseModel):
        id_organizacao: Optional[int] = None
        eh_voluntario: Optional[bool] = None
        eh_gerente: Optional[bool] = None
        primeiro_nome: Optional[constr(max_length=50)] = None
        sobrenome: Optional[constr(max_length=50)] = None
        email: Optional[str] = None
        senha_hash: Optional[constr(max_length=255)] = None
        telefone: Optional[constr(max_length=20)] = None
        deficiencia_auditiva: Optional[bool] = None
        usa_cadeira_rodas: Optional[bool] = None
        deficiencia_cognitiva: Optional[bool] = None
        lgbtq: Optional[bool] = None
        url_imagem_perfil: Optional[str] = None

    class UpdateResponse(BaseModel):
        message: str

    class DeleteResponse(BaseModel):
        message: str
