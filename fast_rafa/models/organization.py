from datetime import datetime
from typing import Dict

from pydantic import BaseModel, EmailStr
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


@table_registry.mapped_as_dataclass
class Organization:
    __tablename__ = 'organizations'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    id_federal: Mapped[str] = mapped_column(
        String(11), nullable=False, unique=True
    )
    nao_governamental: Mapped[bool] = mapped_column(Boolean, nullable=False)
    url_logo: Mapped[str] = mapped_column(
        String(2048), nullable=False, unique=True
    )
    url_imagem: Mapped[str] = mapped_column(
        String(2048), nullable=False, unique=True
    )
    abertura: Mapped[str] = mapped_column(String(20), nullable=False)
    fechamento: Mapped[str] = mapped_column(String(20), nullable=False)
    intervalo: Mapped[str] = mapped_column(String(35), nullable=False)
    nome: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
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
        DateTime, default=datetime.utcnow()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow()
    )

    def __init__(self, **kwargs):
        self.id_federal = kwargs.get('id_federal')
        self.nao_governamental = kwargs.get('nao_governamental')
        self.url_logo = kwargs.get('url_logo')
        self.url_imagem = kwargs.get('url_imagem')
        self.abertura = kwargs.get('abertura')
        self.fechamento = kwargs.get('fechamento')
        self.intervalo = kwargs.get('intervalo')
        self.nome = kwargs.get('nome')
        self.descricao = kwargs.get('descricao')
        self.rua = kwargs.get('rua')
        self.cep = kwargs.get('cep')
        self.cidade = kwargs.get('cidade')
        self.estado = kwargs.get('estado')
        self.telefone = kwargs.get('telefone')
        self.email = kwargs.get('email')

    def to_dict(self):
        return {
            'id': self.id,
            'id_federal': self.id_federal,
            'nao_governamental': self.nao_governamental,
            'url_logo': self.url_logo,
            'url_imagem': self.url_imagem,
            'abertura': self.abertura,
            'fechamento': self.fechamento,
            'intervalo': self.intervalo,
            'nome': self.nome,
            'descricao': self.descricao,
            'rua': self.rua,
            'cep': self.cep,
            'cidade': self.cidade,
            'estado': self.estado,
            'telefone': self.telefone,
            'email': self.email,
            'criado_em': self.criado_em.isoformat()
            if self.criado_em
            else None,
            'atualizado_em': self.atualizado_em.isoformat()
            if self.atualizado_em
            else None,
        }

    employees = relationship(
        'User', back_populates='organization', cascade='all, delete-orphan'
    )

    posts = relationship(
        'Post',
        back_populates='organizations',
        lazy='joined',
        foreign_keys='Post.id_organizacao',
    )

    deliveries_as_org = relationship(
        'Delivery',
        back_populates='organizations',
        foreign_keys='Delivery.id_organizacao',
    )
    deliveries_as_ong = relationship(
        'Delivery', back_populates='ongs', foreign_keys='Delivery.id_ong'
    )

    calendars = relationship('Calendar', back_populates='organizations')

    events = relationship(
        'Event', back_populates='organization', cascade='all, delete-orphan'
    )

    watchlists = relationship('Watchlist', back_populates='organizations')

    @classmethod
    def create(cls, data: 'CreateOrganization') -> 'Organization':
        return cls(**data.dict())

    @classmethod
    def update(cls, instance: 'Organization', data: Dict):
        for key, value in data.items():
            setattr(instance, key, value)
        instance.atualizado_em = datetime.utcnow()
        return instance

    @classmethod
    def delete(cls, id: int):
        return id

    class CreateOrganization(BaseModel):
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

    class UpdateRequestOrganization(BaseModel):
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

    class UpdateResponseOrganization(BaseModel):
        message: str

    class DeleteResponseOrganization(BaseModel):
        message: str
        
    
