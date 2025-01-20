from pydantic import BaseModel


class CreateCategoryMain(BaseModel):
    categoria: str
    slug: str
    icon: str | None = None  # Icon é opcional


class CreateCategory(BaseModel):
    id_categoria_principal: int
    categoria: str
    slug: str
    icon: str | None = None  # Icon é opcional


class CategoryCreateResponse(BaseModel):
    message: str


class CategoryUpdateRequest(BaseModel):
    id_categoria_principal: int
    categoria: str
    slug: str
    icon: str | None = None  # Icon é opcional


class CategoryUpdateResponse(BaseModel):
    message: str


class CategoryDeleteResponse(BaseModel):
    message: str
