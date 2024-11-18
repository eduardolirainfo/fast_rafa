from pydantic import BaseModel, EmailStr


class OrganizationCreate(BaseModel):
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


class OrganizationResponse(BaseModel):
    id: int
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

    @classmethod
    def from_home(cls, organizacao):
        return cls(
            id=organizacao.id,
            id_federal=organizacao.id_federal,
            nao_governamental=organizacao.nao_governamental,
            url_logo=organizacao.url_logo,
            url_imagem=organizacao.url_imagem,
            abertura=organizacao.abertura,
            fechamento=organizacao.fechamento,
            intervalo=organizacao.intervalo,
            nome=organizacao.nome,
            descricao=organizacao.descricao,
            rua=organizacao.rua,
            cep=organizacao.cep,
            cidade=organizacao.cidade,
            estado=organizacao.estado,
            telefone=organizacao.telefone,
            email=organizacao.email,
        )


class OrganizationUpdateRequest(BaseModel):
    id_federal: str = None
    nao_governamental: bool = None
    url_logo: str = None
    url_imagem: str = None
    abertura: str = None
    fechamento: str = None
    intervalo: str = None
    nome: str = None
    descricao: str = None
    rua: str = None
    cep: str = None
    cidade: str = None
    estado: str = None
    telefone: str = None
    email: EmailStr = None


class OrganizationUpdateResponse(OrganizationResponse):
    pass


class OrganizationDeleteResponse(BaseModel):
    message: str
