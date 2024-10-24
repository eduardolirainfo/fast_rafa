from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EventoSchema(BaseModel):
    id: Optional[int]
    nome: str
    dataEvento: datetime

    class Config:
        from_attributes = True
