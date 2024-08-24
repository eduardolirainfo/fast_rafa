from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class MensagemSchema(BaseModel):
    id: Optional[int]
    conteudo: str
    dataEnvio: datetime

    class Config:
        from_attributes = True
