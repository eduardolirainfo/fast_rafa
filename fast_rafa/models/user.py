from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, constr
from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry

from .favorite import Favorite


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[Optional[int]] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    id_organizacao: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey('organizations.id')
    )
    primeiro_nome: Mapped[constr(max_length=50)]
    sobrenome: Mapped[constr(max_length=50)]
    email: Mapped[str] = mapped_column(unique=True)
    senha_hash: Mapped[constr(max_length=255)]
    telefone: Mapped[constr(max_length=20)]
    data_nascimento: Mapped[datetime]
    favoritos: Mapped[List[Favorite]] = relationship(
        'Favorite', back_populates='users'
    )
    deficiencia_auditiva: Mapped[Optional[bool]] = mapped_column(default=None)
    usa_cadeira_rodas: Mapped[Optional[bool]] = mapped_column(default=None)
    deficiencia_cognitiva: Mapped[Optional[bool]] = mapped_column(default=None)
    lgbtq: Mapped[Optional[bool]] = mapped_column(default=None)
    url_imagem_perfil: Mapped[Optional[str]] = mapped_column(default=None)
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now())
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=datetime.now()
    )

    def __init__(
        self,
        id_organizacao: int,
        primeiro_nome: str,
        sobrenome: str,
        email: str,
        senha_hash: str,
        telefone: str,
        data_nascimento: datetime,
        favoritos: Optional[List[Favorite]] = None,
        deficiencia_auditiva: Optional[bool] = None,
        usa_cadeira_rodas: Optional[bool] = None,
        deficiencia_cognitiva: Optional[bool] = None,
        lgbtq: Optional[bool] = None,
        url_imagem_perfil: Optional[str] = None,
        criado_em=None,
        atualizado_em=None
    ):
        self.id_organizacao = id_organizacao
        self.primeiro_nome = primeiro_nome
        self.sobrenome = sobrenome
        self.email = email
        self.senha_hash = senha_hash
        self.telefone = telefone
        self.data_nascimento = data_nascimento
        self.favoritos = []
        self.deficiencia_auditiva = deficiencia_auditiva
        self.usa_cadeira_rodas = usa_cadeira_rodas
        self.deficiencia_cognitiva = deficiencia_cognitiva
        self.lgbtq = lgbtq
        self.url_imagem_perfil = url_imagem_perfil
        self.criado_em = criado_em or datetime.utcnow()
        self.atualizado_em = atualizado_em or datetime.utcnow()

    def to_dict(self):
        return {
            "id": self.id,
            "id_organizacao": self.id_organizacao,
            "primeiro_nome": self.primeiro_nome,
            "sobrenome": self.sobrenome,
            "email": self.email,
            "senha_hash": self.senha_hash,
            "telefone": self.telefone,
            "data_nascimento": self.data_nascimento,
            "favoritos": [favorite.to_dict() for favorite in self.favoritos],
            "deficiencia_auditiva": self.deficiencia_auditiva,
            "usa_cadeira_rodas": self.usa_cadeira_rodas,
            "deficiencia_cognitiva": self.deficiencia_cognitiva,
            "lgbtq": self.lgbtq,
            "url_imagem_perfil": self.url_imagem_perfil,
            "criado_em": self.criado_em,
            "atualizado_em": self.atualizado_em,
        }

    class Create(BaseModel):
        id_organizacao: int
        primeiro_nome: constr(max_length=50)
        sobrenome: constr(max_length=50)
        email: str
        senha_hash: constr(max_length=255)
        telefone: constr(max_length=20)
        data_nascimento: datetime
        favoritos: None
        deficiencia_auditiva: Optional[bool] = None
        usa_cadeira_rodas: Optional[bool] = None
        deficiencia_cognitiva: Optional[bool] = None
        lgbtq: Optional[bool] = None
        url_imagem_perfil: Optional[str] = None
        criado_em: datetime = datetime.utcnow()
        atualizado_em: datetime = datetime.utcnow()

    favorites = relationship(
        'Favorite', back_populates='users'
    )
    organizations = relationship(
        'Organization', back_populates='users')

    posts = relationship(
        'Post', back_populates='users'
    )

    deliveries = relationship(
        'Delivery', back_populates='users'
    )

    @classmethod
    def create(cls, data: Create) -> 'User':
        return cls(
            id_organizacao=data.id_organizacao,
            primeiro_nome=data.primeiro_nome,
            sobrenome=data.sobrenome,
            email=data.email,
            senha_hash=data.senha_hash,
            telefone=data.telefone,
            data_nascimento=data.data_nascimento,
            favoritos=data.favoritos,
            deficiencia_auditiva=data.deficiencia_auditiva,
            usa_cadeira_rodas=data.usa_cadeira_rodas,
            deficiencia_cognitiva=data.deficiencia_cognitiva,
            lgbtq=data.lgbtq,
            url_imagem_perfil=data.url_imagem_perfil,
            criado_em=data.criado_em,
            atualizado_em=data.atualizado_em
        )

    @classmethod
    def model_dump(cls, exclude_unset=False):
        return cls.dict(exclude_unset=exclude_unset)
 
    @classmethod
    def update(cls, instance: 'User', data: Dict):
        for key, value in data.items():
            setattr(instance, key, value)
        return instance

    class UpdateRequest(BaseModel):
        id_organizacao: Optional[int]
        primeiro_nome: Optional[constr(max_length=50)]
        sobrenome: Optional[constr(max_length=50)]
        email: Optional[str]
        senha_hash: Optional[constr(max_length=255)]
        telefone: Optional[constr(max_length=20)]
        data_nascimento: Optional[datetime]
        deficiencia_auditiva: Optional[bool]
        usa_cadeira_rodas: Optional[bool]
        deficiencia_cognitiva: Optional[bool]
        lgbtq: Optional[bool]
        url_imagem_perfil: Optional[str]
        criado_em: Optional[datetime]
        atualizado_em: Optional[datetime]

    class UpdateResponse(BaseModel):
        message: str

    class DeleteResponse(BaseModel):
        message: str
