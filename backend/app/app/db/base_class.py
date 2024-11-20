# Copyright (c) 2022, Eric Lemoine
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

from typing import Annotated, TypeVar

from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, mapped_column


class Base(MappedAsDataclass, DeclarativeBase):
    # pylint: disable=too-few-public-methods
    # type_annotation_map = {decimal.Decimal: SqliteDecimal(scale=2)}
    pass


# ModelType = TypeVar("ModelType", bound=Base)  # pylint: disable=invalid-name


intpk = Annotated[int, mapped_column(primary_key=True)]  # pylint: disable=invalid-name
