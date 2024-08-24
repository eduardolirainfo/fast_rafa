from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EntregaSchema(BaseModel):
    id: Optional[int]
    dataEntrega: datetime
    descricao: str

    class Config:
        from_attributes = True
