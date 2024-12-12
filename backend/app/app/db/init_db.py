from sqlalchemy.orm import Session

from app import crud, schemas
from config import settings
# from app.db.base_class import Base  # noqa: F401
# from app.db import base  # noqa: F401

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


async def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = await crud.user.get_by_email(db, email=settings.FIRST_USER_EMAIL)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_USER_EMAIL,
            username=settings.FIRST_USER_USERNAME,
            password=settings.FIRST_USER_PASSWORD,
            is_active=True,
        )
        user = await crud.user.create(db, obj_in=user_in)
    return user
