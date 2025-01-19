from sqlalchemy.orm import Session

from fast_rafa.modules.categories_main.models import CategoryMain


def get_categories(db: Session):
    return db.query(CategoryMain).all()
