from pydantic import BaseModel


class CreateCategory(BaseModel):
    categoria: str


class CategoryCreateResponse(BaseModel):
    message: str


class CategoryUpdateRequest(BaseModel):
    categoria: str


class CategoryUpdateResponse(BaseModel):
    message: str


class CategoryDeleteResponse(BaseModel):
    message: str
