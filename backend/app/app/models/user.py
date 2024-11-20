# Copyright (c) 2024, Eric Lemoine
# All rights reserved.
# 
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from typing import TYPE_CHECKING, cast

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base, intpk

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
    username: Mapped[str] = mapped_column(String(16), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(64), init=False, nullable=True)
    city: Mapped[str] = mapped_column(String(64), init=False, nullable=True)
    birthdate: Mapped[str] = mapped_column(String(10), init=False, nullable=True)
    gender: Mapped[int] = mapped_column(Integer, init=False, nullable=True)
    photo_path: Mapped[str] = mapped_column(String(254), init=False, nullable=True)
    preferred_language: Mapped[str] = mapped_column(String(10), default="fr-FR")
    access_type: Mapped[int] = mapped_column(Integer, default=1)
    is_active: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)


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
