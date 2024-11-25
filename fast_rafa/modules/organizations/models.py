from datetime import datetime
from typing import Dict

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.modules.base.models import table_registry
from fast_rafa.modules.organizations.schemas import OrganizationCreate
from fast_rafa.utils.timezone import (
    get_local_time_native,
    set_local_time_native,
)


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
        DateTime, default=get_local_time_native
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=get_local_time_native, onupdate=set_local_time_native
    )

    def __init__(self, data: 'OrganizationCreate'):
        for key, value in data.dict().items():
            if hasattr(self, key):
                setattr(self, key, value)

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
    def create(cls, data: 'OrganizationCreate') -> 'Organization':
        return cls(data)

    @classmethod
    def update(cls, instance: 'Organization', data: Dict):
        for key, value in data.items():
            setattr(instance, key, value)
        instance.atualizado_em = get_local_time_native()
        return instance

    @classmethod
    def delete(cls, id: int):
        return id

    @property
    def display_name(self) -> str:
        return f'{self.nome} - {self.cidade}/{self.estado}'
