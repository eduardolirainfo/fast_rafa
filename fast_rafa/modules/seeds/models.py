from sqlalchemy import Boolean, Column, Integer

from fast_rafa.modules.base.models import table_registry


@table_registry.mapped_as_dataclass
class SeedStatus:
    __tablename__ = 'seed_status'

    id = Column(Integer, primary_key=True, index=True)
    seeded = Column(Boolean, default=False)
