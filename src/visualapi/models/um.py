"""Unit of Measures module."""

from sqlmodel import Field, SQLModel

import models


class UnitOfMeasure(SQLModel, table=True):
    """Unit of Measure model."""

    __tablename__ = models.TABLE_NAME_UNIT_OF_MEASURE
    __table_args__ = models.TABLE_ARGS

    rowid: int
    unit_of_measure: str = Field(primary_key=True)
    description: str | None
    scale: int
    category: str | None
    user_defined_uom: str | None
