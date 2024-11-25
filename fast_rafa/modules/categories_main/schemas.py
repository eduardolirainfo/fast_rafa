from pydantic import BaseModel


class CategoryMainCreate(BaseModel):
    categoria: str
    slug: str
    icon: str | None = None


class CategoryMainResponse(BaseModel):
    message: str


class CategoryMainUpdateRequest(BaseModel):
    categoria: str
    slug: str
    icon: str | None = None


class CategoryMainUpdateResponse(BaseModel):
    message: str


class CategoryMainDeleteResponse(BaseModel):
    message: str
