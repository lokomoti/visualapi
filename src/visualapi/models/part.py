"""Part model."""

from pydantic import computed_field
from sqlmodel import Field, SQLModel

import models


class PartBase(SQLModel):
    id: str = Field(primary_key=True, max_length=30)
    description: str | None
    stock_um: str = Field(
        foreign_key=f"{models.SCHEMA}.{models.TABLE_NAME_UNIT_OF_MEASURE}.unit_of_measure"
    )
    product_code: str | None
    commodity_code: str | None
    fabricated: str
    purchased: str
    tool_or_fixture: str
    weight: float | None
    weight_um: str | None = Field(
        foreign_key=f"{models.SCHEMA}.{models.TABLE_NAME_UNIT_OF_MEASURE}.unit_of_measure"
    )
    drawing_id: str | None
    drawing_rev_no: str | None
    drawing_file: str | None
    status: str | None = Field(
        description="Part status is A or O for active or obsolete"
    )

    @computed_field
    @property
    def obsolete(self) -> bool:
        """Check if the part is obsolete."""
        return self.status == "O"


class Part(PartBase, table=True):
    """Part model."""

    __tablename__ = models.TABLE_NAME_PART
    __table_args__ = models.TABLE_ARGS

    rowid: int


class PartPublic(PartBase):
    """Part model for public API."""

    pass
