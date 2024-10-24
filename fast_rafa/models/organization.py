from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, EmailStr
from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


@table_registry.mapped_as_dataclass
class Organization:
    __tablename__ = 'organizations'

    id: Mapped[Optional[int]] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    id_federal: Mapped[str] = mapped_column(
        String(11), nullable=False, unique=True)
    nao_governamental: Mapped[bool] = mapped_column(Boolean, nullable=False)
    url_logo: Mapped[str] = mapped_column(
        String(2048), nullable=False, unique=True)
    url_imagem: Mapped[str] = mapped_column(
        String(2048), nullable=False, unique=True)
    abertura: Mapped[str] = mapped_column(String(20), nullable=False)
    fechamento: Mapped[str] = mapped_column(String(20), nullable=False)
    intervalo: Mapped[str] = mapped_column(String(35), nullable=False)
    nome: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True)
    descricao: Mapped[str] = mapped_column(String(1000), nullable=False)
    rua: Mapped[str] = mapped_column(String(100), nullable=False)
    cep: Mapped[str] = mapped_column(String(18), nullable=False)
    cidade: Mapped[str] = mapped_column(String(17), nullable=False)
    estado: Mapped[str] = mapped_column(String(12), nullable=False)
    telefone: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=True
    )
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now())
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=datetime.now()
    )

    def __init__(self, id_federal, nao_governamental,
                 url_logo, url_imagem, abertura,
                 fechamento, intervalo, nome, descricao,
                 rua, cep, cidade, estado,
                 telefone, email, criado_em=None, atualizado_em=None):
        self.id_federal = id_federal
        self.nao_governamental = nao_governamental
        self.url_logo = url_logo
        self.url_imagem = url_imagem
        self.abertura = abertura
        self.fechamento = fechamento
        self.intervalo = intervalo
        self.nome = nome
        self.descricao = descricao
        self.rua = rua
        self.cep = cep
        self.cidade = cidade
        self.estado = estado
        self.telefone = telefone
        self.email = email
        self.criado_em = criado_em or datetime.utcnow()
        self.atualizado_em = atualizado_em or datetime.utcnow()

    def to_dict(self):
        return {
            "id": self.id,
            "id_federal": self.id_federal,
            "nao_governamental": self.nao_governamental,
            "url_logo": self.url_logo,
            "url_imagem": self.url_imagem,
            "abertura": self.abertura,
            "fechamento": self.fechamento,
            "intervalo": self.intervalo,
            "nome": self.nome,
            "descricao": self.descricao,
            "rua": self.rua,
            "cep": self.cep,
            "cidade": self.cidade,
            "estado": self.estado,
            "telefone": self.telefone,
            "email": self.email,
            "criado_em": self.criado_em.isoformat()
            if self.criado_em else None,
            "atualizado_em": self.atualizado_em.isoformat()
            if self.atualizado_em else None,
        }

    users = relationship(
        'User',
        back_populates='organizations',
        lazy='joined',
        foreign_keys='User.id_organizacao',
    )

    posts = relationship(
        'Post',
        back_populates='organizations',
        lazy='joined',
        foreign_keys='Post.id_organizacao',
    )

    deliveries = relationship("Delivery", back_populates="organizations")

    @classmethod
    def model_dump(cls, exclude_unset=False):
        return cls.dict(exclude_unset=exclude_unset)

    @classmethod
    def update(cls, instance: 'Organization', data: Dict):
        for key, value in data.items():
            setattr(instance, key, value)
        instance.atualizado_em = datetime.utcnow()
        return instance

    @classmethod
    def delete(cls, id: int):
        return cls.objects.filter(id=id).delete()

    @classmethod
    def last(cls):
        return cls.objects.last()

    class Create(BaseModel):
        id_federal: str
        nao_governamental: bool
        url_logo: str
        url_imagem: str
        abertura: str
        fechamento: str
        intervalo: str
        nome: str
        descricao: str
        rua: str
        cep: str
        cidade: str
        estado: str
        telefone: str
        email: EmailStr
        criado_em: datetime = datetime.utcnow()
        atualizado_em: datetime = datetime.utcnow()

    @classmethod
    def create(cls, data: Create) -> 'Organization':
        new_org = cls(
            id_federal=data.id_federal,
            nao_governamental=data.nao_governamental,
            url_logo=data.url_logo,
            url_imagem=data.url_imagem,
            abertura=data.abertura,
            fechamento=data.fechamento,
            intervalo=data.intervalo,
            nome=data.nome,
            descricao=data.descricao,
            rua=data.rua,
            cep=data.cep,
            cidade=data.cidade,
            estado=data.estado,
            telefone=data.telefone,
            email=data.email,
            criado_em=data.criado_em,
            atualizado_em=data.atualizado_em,
        )
        return new_org

    class UpdateRequest(BaseModel):
        id_federal: str
        nao_governamental: bool
        url_logo: str
        url_imagem: str
        abertura: str
        fechamento: str
        intervalo: str
        nome: str
        descricao: str
        rua: str
        cep: str
        cidade: str
        estado: str
        telefone: str
        email: EmailStr

    class UpdateResponse(BaseModel):
        message: str

    class DeleteResponse(BaseModel):
        message: str
