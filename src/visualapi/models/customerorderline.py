"""Customer order line model."""

from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

import models
from models.part import Part, PartPublic


class CustomerOrderLineBase(SQLModel):
    """Customer order line base model."""

    cust_order_id: str = Field(
        max_length=15,
        primary_key=True,
        foreign_key=f"{models.SCHEMA}.{models.TABLE_NAME_CUSTOMER_ORDER}.id",
    )
    line_no: int = Field(primary_key=True)
    part_id: str | None = Field(
        foreign_key=f"{models.SCHEMA}.{models.TABLE_NAME_PART}.id"
    )
    customer_part_id: str | None
    line_status: str
    order_qty: float
    user_order_qty: float
    selling_um: str | None = Field(
        foreign_key=f"{models.SCHEMA}.{models.TABLE_NAME_UNIT_OF_MEASURE}.unit_of_measure"
    )
    unit_price: float
    misc_reference: str | None
    product_code: str | None
    commodity_code: str | None
    warehouse_id: str | None
    site_id: str = Field(
        foreign_key=f"{models.SCHEMA}.{models.TABLE_NAME_SITE}.id",
    )
    entered_by: str | None

    # Dates
    desired_ship_date: datetime | None
    promise_date: datetime | None
    last_shipped_date: datetime | None


class CustomerOrderLine(CustomerOrderLineBase, table=True):
    """Customer order line model."""

    __tablename__ = models.TABLE_NAME_CUSTOMER_ORDER_LINE
    __table_args__ = models.TABLE_ARGS

    part: "Part" = Relationship()


class CustomerOrderLineWithPartPublic(CustomerOrderLineBase):
    """Customer order line public model."""

    part: PartPublic | None


class CustomerOrderLinePublic(CustomerOrderLineBase):
    """Customer order line public model."""

    pass
