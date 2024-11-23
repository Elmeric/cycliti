from typing import Any, Dict, Optional, Union
from uuid import uuid4
from datetime import datetime as dt
from datetime import timezone

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase, CrudError, CrudIntegrityError
from app.models.user import Activation, User
from app.schemas.user import UserCreate, UserUpdate
from tests.api.api_v1.test_login import test_reset_password_success
from utils import generate_nonce


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_uid(self, db: Session, *, uid: str) -> Optional[User]:
        return db.scalars(select(User).filter(User.uid == uid)).first()

    async def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.scalars(select(User).filter(User.email == email)).first()

    async def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.scalars(select(User).filter(User.username == username)).first()

    async def create(self, db: Session, *, obj_in: UserCreate) -> User:
        hashed_pwd = get_password_hash(obj_in.password.get_secret_value())
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data["uid"] = uuid4().hex
        del obj_in_data["password"]
        obj_in_data["hashed_password"] = hashed_pwd
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        try:
            db.commit()
        except SQLAlchemyError as exc:
            db.rollback()
            raise CrudError() from exc
        db.refresh(db_obj)
        return db_obj

    async def pre_activate(self, db: Session, *, db_obj: User) -> User:
        nonce = generate_nonce()
        timestamp = int(dt.timestamp(dt.now(timezone.utc)))
        print(f"Nonce: {nonce}")
        print(f"Timestamp: {timestamp}")
        db_obj.activation = Activation(nonce=nonce, issued_at=timestamp)
        try:
            db.commit()
        except SQLAlchemyError as exc:
            db.rollback()
            raise CrudError() from exc
        db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return await super().update(db, db_obj=db_obj, obj_in=update_data)

    async def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user_db = await self.get_by_email(db, email=email)
        if not user_db:
            return None
        if not verify_password(password, user_db.hashed_password):
            return None
        return user_db

    async def activate(self, db: Session, *, db_obj: User):
        db_obj.is_active = True
        db_obj.activation = None
        db.add(db_obj)
        try:
            db.commit()
        except SQLAlchemyError as exc:
            db.rollback()
            raise CrudError() from exc

    async def change_password(self, db: Session, *, user_db: User, new_password: str):
        hashed_password = get_password_hash(new_password)
        user_db.hashed_password = hashed_password
        db.add(user_db)
        try:
            db.commit()
        except SQLAlchemyError as exc:
            db.rollback()
            raise CrudError() from exc

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
