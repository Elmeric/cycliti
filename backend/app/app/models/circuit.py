# Copyright (c) 2024, Eric Lemoine
# All rights reserved.
# 
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from geoalchemy2 import WKBElement, Geometry
from sqlalchemy import (
    String, Integer, ForeignKey, Text, DECIMAL,
    DateTime, Table, Column
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, intpk

if TYPE_CHECKING:  # pragma: no cover
    from app.models.user import User
    from app.models.graph import Edge


circuit_edge = Table(
    "circuit_edge",
    Base.metadata,
    Column("circuit_id", ForeignKey("circuit.id"), primary_key=True),
    Column("edge_id", ForeignKey("edge.id"), primary_key=True),
)


class Circuit(Base):
    # pylint: disable=too-few-public-methods
    __tablename__ = "circuit"
    __table_args__ = {"mysql_engine": "InnoDB"}

    id: Mapped[intpk] = mapped_column(init=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        init=False,
        nullable=False,
        unique=True,
        index=True,
        comment="User ID the circuit belongs to"
    )
    name: Mapped[str | None] = mapped_column(
        String(250), comment="Activity name (May include spaces)"
    )
    description: Mapped[str | None] = mapped_column(
        Text, comment="Activity description (May include spaces)",
    )
    distance: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="Distance in meters"
    )
    start_time: Mapped[str] = mapped_column(
        DateTime, nullable=False, comment="Activity start date (datetime)"
    )
    start_point: Mapped[WKBElement] = mapped_column(Geometry(
        geometry_type="POINT", srid=4326)
    )
    end_time: Mapped[str] = mapped_column(
        DateTime, nullable=False, comment="Activity end date (datetime)"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, comment="Activity creation date (datetime)"
    )
    elevation_gain: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="Elevation gain in meters"
    )
    elevation_loss: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="Elevation loss in meters"
    )
    average_speed: Mapped[Decimal] = mapped_column(
        DECIMAL(precision=4, scale=2),
        nullable=False,
        comment="Average speed meter per second (m/s)",
    )
    trace: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="LINESTRING", srid=4326),
        nullable=False,
        comment="A LINESTRING built from the GPS measured track, in WGS 84 lat/long (4326)",
    )

    user: Mapped["User"] = relationship(
        init=False,
        back_populates="circuits",
    )
    edges: Mapped[list["Edge"]] = relationship(
        secondary=circuit_edge,
        back_populates="circuits"
    )
