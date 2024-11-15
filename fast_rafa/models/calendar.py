from datetime import datetime
from typing import Dict

from pydantic import BaseModel
from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from fast_rafa.models.base import table_registry


@table_registry.mapped_as_dataclass
class Calendar:
    """Modelo que representa um calendário para uma organização.

    Atributos:
        id (int): Identificador único do calendário.
        id_organizacao (int): Chave estrangeira que referencia a
            organização.
        abertura (datetime): Data e hora de abertura do calendário.
        fechamento (datetime): Data e hora de fechamento do calendário.
        criado_em (datetime): Timestamp que indica quando o calendário foi
            criado.
        atualizado_em (datetime): Timestamp que indica quando o calendário
            foi atualizado pela última vez.
    """

    __tablename__ = 'calendars'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    id_organizacao: Mapped[int] = mapped_column(
        Integer, ForeignKey('organizations.id'), unique=True, nullable=False
    )
    abertura: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow()
    )
    fechamento: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow()
    )
    criado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow()
    )
    atualizado_em: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow()
    )

    def __init__(
        self,
        id_organizacao,
        abertura,
        fechamento,
        criado_em=None,
        atualizado_em=None,
    ):
        """Inicializa uma instância de Calendar.

        Args:
            id_organizacao (int): O ID da organização.
            abertura (datetime): A data e hora de abertura.
            fechamento (datetime): A data e hora de fechamento.
            criado_em (datetime, optional): O timestamp de criação. Padrão
                é a hora atual em UTC.
            atualizado_em (datetime, optional): O timestamp de última
                atualização. Padrão é a hora atual em UTC.
        """
        self.id_organizacao = id_organizacao
        self.abertura = abertura
        self.fechamento = fechamento
        self.criado_em = criado_em or datetime.utcnow()
        self.atualizado_em = atualizado_em or datetime.utcnow()

    def to_dict(self):
        """Converte a instância de Calendar para um dicionário.

        Returns:
            dict: Uma representação em dicionário da instância do
                calendário.
        """
        return {
            'id': self.id,
            'id_organizacao': self.id_organizacao,
            'abertura': self.abertura.isoformat(),
            'fechamento': self.fechamento.isoformat(),
            'criado_em': self.criado_em.isoformat(),
            'atualizado_em': self.atualizado_em.isoformat()
            if self.atualizado_em
            else None,
        }

    organizations = relationship('Organization', back_populates='calendars')

    class CreateCalendar(BaseModel):
        """Modelo de dados para criar uma nova instância de Calendar.

        Atributos:
            id_organizacao (int): O ID da organização.
            abertura (datetime): A data e hora de abertura.
            fechamento (datetime): A data e hora de fechamento.
            criado_em (datetime): O timestamp de criação. Padrão é a
                hora atual em UTC.
            atualizado_em (datetime): O timestamp de última atualização.
                Padrão é a hora atual em UTC.
        """

        id_organizacao: int
        abertura: datetime
        fechamento: datetime
        criado_em: datetime = datetime.utcnow()
        atualizado_em: datetime = datetime.utcnow()

    class UpdateRequestCalendar(BaseModel):
        """Modelo de dados para atualizar uma instância existente de Calendar.

        Atributos:
            id_organizacao (int): O ID da organização.
            abertura (datetime): A data e hora de abertura.
            fechamento (datetime): A data e hora de fechamento.
        """

        id_organizacao: int
        abertura: datetime
        fechamento: datetime

    class UpdateResponseCalendar(BaseModel):
        """Modelo de resposta para a atualização de uma instância de Calendar.

        Atributos:
            message (str): Mensagem de confirmação da atualização.
        """

        message: str

    class DeleteResponseCalendar(BaseModel):
        """Modelo de resposta para a deleção de uma instância de Calendar.

        Atributos:
            message (str): Mensagem de confirmação da deleção.
        """

        message: str

    @classmethod
    def create(cls, data: CreateCalendar) -> 'Calendar':
        """Cria uma nova instância de Calendar a partir dos dados fornecidos.

        Args:
            data (Create): Os dados usados para criar a nova instância.

        Returns:
            Calendar: A nova instância de Calendar criada.
        """
        return cls(
            id_organizacao=data.id_organizacao,
            abertura=data.abertura,
            fechamento=data.fechamento,
            criado_em=data.criado_em,
            atualizado_em=data.atualizado_em,
        )

    @classmethod
    def update(cls, instance: 'Calendar', data: Dict):
        """Atualiza a instância de Calendar especificada com novos dados.

        Args:
            instance (Calendar): A instância de Calendar a ser atualizada.
            data (Dict): Um dicionário contendo os campos a serem
                atualizados.

        Returns:
            Calendar: A instância de Calendar atualizada.
        """
        for key, value in data.items():
            setattr(instance, key, value)
        instance.atualizado_em = datetime.utcnow()
        return instance
