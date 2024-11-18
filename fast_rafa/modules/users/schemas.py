from typing import Optional

from pydantic import BaseModel, constr


class CreateUser(BaseModel):
    id_organizacao: int
    eh_deletado: bool = False
    eh_voluntario: bool = False
    eh_gerente: bool = False
    primeiro_nome: constr(max_length=50)
    sobrenome: constr(max_length=50)
    email: str
    username: str
    senha_hash: constr(max_length=255)
    telefone: constr(max_length=20)
    deficiencia_auditiva: Optional[bool] = None
    usa_cadeira_rodas: Optional[bool] = None
    deficiencia_cognitiva: Optional[bool] = None
    lgbtq: Optional[bool] = None
    url_imagem_perfil: Optional[str] = None


class UpdateUserRequest(BaseModel):
    id_organizacao: Optional[int] = None
    eh_deletado: Optional[bool] = None
    eh_voluntario: Optional[bool] = None
    eh_gerente: Optional[bool] = None
    primeiro_nome: Optional[constr(max_length=50)] = None
    sobrenome: Optional[constr(max_length=50)] = None
    email: Optional[str] = None
    username: Optional[str] = None
    senha_hash: Optional[constr(max_length=255)] = None
    telefone: Optional[constr(max_length=20)] = None
    deficiencia_auditiva: Optional[bool] = None
    usa_cadeira_rodas: Optional[bool] = None
    deficiencia_cognitiva: Optional[bool] = None
    lgbtq: Optional[bool] = None
    url_imagem_perfil: Optional[str] = None


class CreateUserResponse(BaseModel):
    message: str


class DeleteUserResponse(BaseModel):
    message: str


class UserResponse(BaseModel):
    id: int
    primeiro_nome: str
    sobrenome: str
    email: str
    url_imagem_perfil: str = ''
    id_organizacao: Optional[int] = None
    eh_deletado: bool
    eh_voluntario: bool
    eh_gerente: bool

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


class UpdateUserResponse(UserResponse):
    pass
