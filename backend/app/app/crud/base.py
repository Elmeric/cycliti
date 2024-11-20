from typing import Any, Generic, Optional, Type, TypeVar, cast

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CrudError(Exception):
    pass


class CrudIntegrityError(CrudError):
    pass


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """ CRUD object with default methods to Create, Read, Update, Delete (CRUD)."""
        self.model = model

    async def get(self, db: Session, obj_id: Any) -> Optional[ModelType]:
        try:
            obj = db.get(self.model, obj_id)
        except SQLAlchemyError as exc:
            raise CrudError from exc
        return obj

    async def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        try:
            obj_list = cast(
                list[ModelType],
                db.scalars(select(self.model).offset(skip).limit(limit)).all(),
            )
        except SQLAlchemyError as exc:
            raise CrudError from exc
        return obj_list

    async def get_all(self, db: Session) -> list[ModelType]:
        try:
            obj_list = db.query(self.model).all()
            obj_list = cast(
                list[ModelType], db.scalars(select(self.model)).all()
            )
        except SQLAlchemyError as exc:
            raise CrudError from exc
        return obj_list

    async def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        try:
            db.commit()
        except SQLAlchemyError as exc:
            db.rollback()
            raise CrudError() from exc
        db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        updated = False
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if (
                field in update_data
                and update_data[field] is not None
                and getattr(db_obj, field) != update_data[field]
            ):
                setattr(db_obj, field, update_data[field])
                updated = True

        if updated:
            try:
                db.commit()
            except SQLAlchemyError as exc:
                db.rollback()
                raise CrudError() from exc
            db.refresh(db_obj)
            return db_obj
        return db_obj

    async def delete(self, db: Session, *, db_obj: ModelType) -> ModelType:
        # db_obj = db.get(self.model, obj_id)
        db.delete(db_obj)
        try:
            db.commit()
        except IntegrityError as exc:
            db.rollback()
            raise CrudIntegrityError() from exc
        except SQLAlchemyError as exc:
            db.rollback()
            raise CrudError() from exc
        return db_obj
