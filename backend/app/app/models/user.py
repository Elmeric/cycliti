# Copyright (c) 2024, Eric Lemoine
# All rights reserved.
# 
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from typing import TYPE_CHECKING, cast

from sqlalchemy import String, Integer, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, intpk
from schemas.user import GenderEnum


# Refer to: https://github.com/dropbox/sqlalchemy-stubs/issues/98#issuecomment-762884766
# if TYPE_CHECKING:
#     hybrid_property = property  # pylint: disable=invalid-name
# else:
#     from sqlalchemy.ext.hybrid import hybrid_property


class User(Base):
    # pylint: disable=too-few-public-methods
    __tablename__ = "user"

    id: Mapped[intpk] = mapped_column(init=False)
    uid: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(16))
    hashed_password: Mapped[str] = mapped_column(Text)
    name: Mapped[str | None] = mapped_column(String(64), init=False)
    city: Mapped[str | None] = mapped_column(String(64), init=False, )
    birthdate: Mapped[str | None] = mapped_column(String(10), init=False)
    gender: Mapped[GenderEnum | None] = mapped_column(init=False)
    photo_path: Mapped[str | None] = mapped_column(String(254), init=False)
    preferred_language: Mapped[str] = mapped_column(String(10), default="fr-FR")
    access_type: Mapped[int] = mapped_column(Integer, default=1)
    is_active: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    activation: Mapped["Activation"] = relationship(
        init=False,
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Activation(Base):
    # pylint: disable=too-few-public-methods
    __tablename__ = "activation"

    id: Mapped[intpk] = mapped_column(init=False)
    nonce: Mapped[str] = mapped_column(Text)
    issued_at: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), init=False)

    user: Mapped["User"] = relationship(
        back_populates="activation",
        init=False,
        single_parent=True,
    )

    __table_args__ = (UniqueConstraint("user_id"),)

    # basket: Mapped["Basket"] = relationship(
    #     init=False,
    #     back_populates="client"
    #     # cascade="all, delete-orphan"
    #     # init=False, back_populates="client", cascade="all, delete-orphan"
    # )
    # invoices: Mapped[list["Invoice"]] = relationship(
    #     init=False,
    #     back_populates="client",
    #     # cascade="all, delete-orphan",
    # )
    #
    # @hybrid_property
    # def has_emitted_invoices(self) -> bool:
    #     return any(invoice.status != InvoiceStatus.DRAFT for invoice in self.invoices)
    #
    # @has_emitted_invoices.expression
    # def has_emitted_invoices(self):  # type: ignore
    #     return select(
    #         case(
    #             (
    #                 exists()
    #                 .where(
    #                     and_(
    #                         Invoice.client_id == self.id,
    #                         Invoice.status != "DRAFT",
    #                     )
    #                 )
    #                 .correlate(self),  # type: ignore
    #                 True,
    #             ),
    #             else_=False,
    #         ).label("has_emitted_invoices")
    #     ).scalar_subquery()
    #
    # def __post_init__(self) -> None:
    #     self.basket = cast(Mapped[Basket], Basket())
