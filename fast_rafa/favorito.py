from typing import List, Optional

from pydantic import BaseModel


class FavoriteSchema(BaseModel):
    id: Optional[int] = None
    idPostagem: int = None
    idUsuario: int = None

    @staticmethod
    def get_all() -> List['FavoriteSchema']:
        return []

    @property
    def usuario(self):
        from .user import UserSchema  # noqa: PLC0415

        return UserSchema(id=self.idUsuario)

    @property
    def postagem(self):
        from .post import PostSchema  # noqa: PLC0415

        return PostSchema(id=self.idPostagem)
