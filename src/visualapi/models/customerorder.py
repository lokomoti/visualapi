"""Customer order model."""

from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

import models
from models.customer import Customer, CustomerPublic
from models.customerorderline import CustomerOrderLine, CustomerOrderLinePublic


class CustomerOrderBase(SQLModel):
    """Base class for customer order model."""

    id: str = Field(primary_key=True, max_length=15)
    customer_id: str = Field(
        foreign_key=f"{models.SCHEMA}.{models.TABLE_NAME_CUSTOMER}.id"
    )
    customer_po_ref: str | None
    free_on_board: str | None
    ship_via: str | None
    territory: str | None
    site_id: str = Field(foreign_key=f"{models.SCHEMA}.{models.TABLE_NAME_SITE}.id")
    status: str
    total_amt_ordered: float
    total_amt_shipped: float
    currency_id: str = Field(
        foreign_key=f"{models.SCHEMA}.{models.TABLE_NAME_CURRENCY}.id"
    )

    # Dates
    order_date: datetime
    desired_ship_date: datetime | None
    last_shipped_date: datetime | None
    promise_date: datetime | None
    create_date: datetime


class CustomerOrder(CustomerOrderBase, table=True):
    """Customer order model."""

    __tablename__ = models.TABLE_NAME_CUSTOMER_ORDER
    __table_args__ = models.TABLE_ARGS

    rowid: int

    order_lines: list["CustomerOrderLine"] = Relationship()
    customer: "Customer" = Relationship()


class CustomerOrderPublic(CustomerOrderBase):
    """Public customer order model."""

    order_lines: list[CustomerOrderLinePublic]
    customer: CustomerPublic
