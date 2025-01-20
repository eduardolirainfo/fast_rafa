import enum
import re
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, constr, validator

from fast_rafa.core.logger import setup_logger

logger = setup_logger()


class SexoEnum(str, enum.Enum):
    MASCULINO = 'M'
    FEMININO = 'F'
    OUTRO = 'O'
    NAO_INFORMADO = 'NI'


class TelefoneValidator:
    valid_ddds = [
        '11',
        '12',
        '13',
        '14',
        '15',
        '16',
        '17',
        '18',
        '19',
        '21',
        '22',
        '24',
        '27',
        '28',
        '31',
        '32',
        '33',
        '34',
        '35',
        '37',
        '38',
        '41',
        '42',
        '43',
        '44',
        '45',
        '46',
        '47',
        '48',
        '49',
        '51',
        '52',
        '53',
        '54',
        '55',
        '61',
        '62',
        '63',
        '64',
        '65',
        '66',
        '67',
        '68',
        '69',
        '71',
        '73',
        '74',
        '75',
        '77',
        '79',
        '81',
        '82',
        '83',
        '84',
        '85',
        '86',
        '87',
        '88',
        '89',
        '91',
        '92',
        '93',
        '94',
        '95',
        '96',
        '97',
        '98',
        '99',
    ]

    @staticmethod
    def validate(value: str) -> str:
        telefone_sem_mascara = re.sub(r'\D', '', value)
        monze = 11

        if len(telefone_sem_mascara) != monze:
            raise ValueError('O número de telefone deve conter 11 dígitos.')

        numero_sem_ddd = telefone_sem_mascara[2:]

        if numero_sem_ddd == '0' * len(numero_sem_ddd):
            raise ValueError(
                'O número de telefone não pode ser composto apenas por zeros.'
            )

        ddd = telefone_sem_mascara[:2]
        if ddd not in TelefoneValidator.valid_ddds:
            raise ValueError(f'O DDD {ddd} não é válido.')

        return value


class CreateUser(BaseModel):
    id_organizacao: int
    eh_deletado: bool = False
    eh_voluntario: bool = False
    eh_gerente: bool = False
    primeiro_nome: constr(max_length=50)
    sobrenome: constr(max_length=50)
    email: EmailStr
    username: constr(max_length=50)
    senha_hash: str
    telefone: constr(max_length=20)
    deficiencia_auditiva: Optional[bool] = None
    usa_cadeira_rodas: Optional[bool] = None
    deficiencia_cognitiva: Optional[bool] = None
    lgbtq: Optional[bool] = None
    url_imagem_perfil: str | None = None
    aniversario: Optional[date] = None
    sexo: Optional[SexoEnum] = None

    @validator('aniversario', pre=True)
    def parse_date(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError(
                    'Data inválida. O formato esperado é YYYY-MM-DD.'
                )
        return value

    # @validator('telefone', pre=True, always=True)
    # def sanitize_phone(cls, value: str) -> str:
    #     if value:
    #         return re.sub(r'\D', '', value)
    #     return value

    @validator('telefone')
    def validate_telefone_field(cls, value):
        return TelefoneValidator.validate(value)


class UpdateUserRequest(BaseModel):
    id_organizacao: Optional[int] = None
    eh_deletado: Optional[bool] = None
    eh_voluntario: Optional[bool] = None
    eh_gerente: Optional[bool] = None
    primeiro_nome: Optional[constr(max_length=50)] = None
    sobrenome: Optional[constr(max_length=50)] = None
    email: Optional[str] = None
    username: Optional[str] = None
    senha_hash: Optional[str] = None
    telefone: Optional[constr(max_length=20)] = None
    deficiencia_auditiva: Optional[bool] = None
    usa_cadeira_rodas: Optional[bool] = None
    deficiencia_cognitiva: Optional[bool] = None
    lgbtq: Optional[bool] = None
    url_imagem_perfil: Optional[str] = None
    aniversario: Optional[date] = None
    sexo: Optional[SexoEnum] = None

    @validator('telefone', always=True)
    def validate_telefone_field(cls, value):
        if value:
            return TelefoneValidator.validate(value)
        return value


class CreateUserResponse(BaseModel):
    message: str


class DeleteUserResponse(BaseModel):
    message: str


class UserResponse(BaseModel):
    id: int
    primeiro_nome: str
    sobrenome: str
    email: str
    telefone: Optional[str] = None
    url_imagem_perfil: Optional[str] = None
    id_organizacao: Optional[int]
    eh_deletado: bool
    eh_voluntario: bool
    eh_gerente: bool
    lgbtq: Optional[bool] = None
    deficiencia_auditiva: Optional[bool] = None
    deficiencia_cognitiva: Optional[bool] = None
    usa_cadeira_rodas: Optional[bool] = None
    aniversario: Optional[date] = None
    sexo: Optional[SexoEnum] = None

    @classmethod
    def from_home(cls, usuario):
        url_imagem = (
            usuario.url_imagem_perfil if usuario.url_imagem_perfil else ''
        )
        return cls(
            id=usuario.id,
            primeiro_nome=usuario.primeiro_nome,
            sobrenome=getattr(usuario, 'sobrenome', 'Nome não disponível'),
            email=usuario.email,
            url_imagem_perfil=url_imagem,
            id_organizacao=usuario.id_organizacao
            if hasattr(usuario, 'id_organizacao')
            else None,
            eh_deletado=usuario.eh_deletado
            if hasattr(usuario, 'eh_deletado')
            else False,
            eh_voluntario=usuario.eh_voluntario
            if hasattr(usuario, 'eh_voluntario')
            else False,
            eh_gerente=usuario.eh_gerente
            if hasattr(usuario, 'eh_gerente')
            else False,
        )

    @classmethod
    def from_profile(cls, usuario):
        url_imagem = (
            usuario.url_imagem_perfil if usuario.url_imagem_perfil else ''
        )
        return cls(
            id=usuario.id,
            id_organizacao=usuario.id_organizacao,
            eh_deletado=usuario.eh_deletado,
            eh_voluntario=usuario.eh_voluntario,
            eh_gerente=usuario.eh_gerente,
            primeiro_nome=usuario.primeiro_nome,
            sobrenome=usuario.sobrenome,
            email=usuario.email,
            telefone=usuario.telefone,
            url_imagem_perfil=url_imagem,
        )

    @validator('telefone', pre=False, always=True)
    def format_phone(cls, value: Optional[str]) -> Optional[str]:
        mdez = 10
        monze = 11
        if value and len(value) == monze:
            return f'({value[:2]}) {value[2:7]}-{value[7:]}'
        elif value and len(value) == mdez:
            return f'({value[:2]}) {value[2:6]}-{value[6:]}'
        return value


class UpdateUserResponse(UserResponse):
    pass
