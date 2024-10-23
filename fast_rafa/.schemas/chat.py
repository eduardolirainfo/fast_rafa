from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ChatSchema(BaseModel):
    id: Optional[int]
    conteudo: str
    dataEnvio: datetime
