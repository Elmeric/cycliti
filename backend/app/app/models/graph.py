# Copyright (c) 2024, Eric Lemoine
# All rights reserved.
# 
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
from typing import TYPE_CHECKING

from geoalchemy2 import WKBElement, Geometry
from sqlalchemy import Integer, ForeignKey, Text, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, intpk
from app.models.circuit import circuit_edge

if TYPE_CHECKING:  # pragma: no cover
    from app.models.circuit import Circuit


class Graph(Base):
    """ A geo-referenced directed multigraph """
    # pylint: disable=too-few-public-methods
    __tablename__ = "graph"
    __table_args__ = {"mysql_engine": "InnoDB"}

    id: Mapped[intpk] = mapped_column(init=False)
    crs: Mapped[str] = mapped_column(
        Text,
        init=True,
        nullable=False,
        comment="A shapely CRS in WKT format"
    )

    nodes: Mapped[list["Node"]] = relationship(
        init=False,
        back_populates="graph",
        cascade="all, delete, delete-orphan"
    )
    edges: Mapped[list["Edge"]] = relationship(
        init=False,
        back_populates="graph",
        cascade="all, delete, delete-orphan"
    )


class Node(Base):
    # pylint: disable=too-few-public-methods
    __tablename__ = "node"
    __table_args__ = {"mysql_engine": "InnoDB"}

    id: Mapped[intpk] = mapped_column(init=False)
    graph_id: Mapped[int] = mapped_column(
        ForeignKey("graph.id"),
        nullable=False,
        index=True,
    )
    location: Mapped[WKBElement] = mapped_column(Geometry(
        geometry_type="POINT", srid=4326)
    )

    # location: Mapped[str] = mapped_column(
    #     Text,
    #     init=True,
    #     nullable=False,
    #     comment="A shapely POINT in WKT format"
    # )

    graph: Mapped["Graph"] = relationship(
        init=False,
        back_populates="nodes",
    )


class Edge(Base):
    # pylint: disable=too-few-public-methods
    __tablename__ = "edge"
    # __table_args__ = {"mysql_engine": "InnoDB"}
    __table_args__ = (
        Index('edge_index', "source_id", "target_id", "key"),
        {"mysql_engine": "InnoDB"},
    )

    id: Mapped[intpk] = mapped_column(init=False)
    graph_id: Mapped[int] = mapped_column(
        ForeignKey("graph.id"),
        nullable=False,
        index=True,
    )
    source_id: Mapped[int] = mapped_column(
        ForeignKey("node.id"),
        nullable=False,
        index=True,
    )
    target_id: Mapped[int] = mapped_column(
        ForeignKey("node.id"),
        nullable=False,
        index=True,
    )
    key: Mapped[int] = mapped_column(
        Integer,
        init=True,
        nullable=False,
    )
    geometry: Mapped[WKBElement] = mapped_column(
        Geometry(geometry_type="LINESTRING", srid=4326)
    )

    # geometry: Mapped[str] = mapped_column(
    #     Text,
    #     init=True,
    #     nullable=False,
    #     comment="A shapely LINESTRING in WKT format"
    # )
    reversed: Mapped[bool] = mapped_column(
        Boolean,
        init=True,
        nullable=False,
        comment="If True, the LINESTRING geometry shall be reversed in forward traversal"
    )
    length: Mapped[int] = mapped_column(
        Integer,
        init=True,
        nullable=False,
        comment="in meter"
    )
    positive_elevation: Mapped[int] = mapped_column(
        Integer,
        init=True,
        nullable=False,
        comment="in meter"
    )
    negative_elevation: Mapped[int] = mapped_column(
        Integer,
        init=True,
        nullable=False,
        comment="in meter"
    )
    # popularity: Mapped[int] = mapped_column(
    #     Integer,
    #     init=False,
    #     default=0,
    #     nullable=False,
    # )

    graph: Mapped["Graph"] = relationship(
        init=False,
        back_populates="edges",
    )
    circuits: Mapped[list["Circuit"]] = relationship(
        init=False,
        secondary=circuit_edge,
        back_populates="edges"
    )
