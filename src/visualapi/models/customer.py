"""Customer model."""

from sqlmodel import Field, SQLModel

import models


class CustomerBase(SQLModel):
    """Base class for Customer model."""

    id: str = Field(primary_key=True, max_length=15)
    name: str | None
    addr_1: str | None
    addr_2: str | None
    addr_3: str | None
    city: str | None
    state: str | None
    zipcode: str | None
    country: str | None
    country_id: str | None  # This is FK


class Customer(CustomerBase, table=True):
    """Customer model."""

    __tablename__ = models.TABLE_NAME_CUSTOMER
    __table_args__ = models.TABLE_ARGS

    rowid: int


class CustomerPublic(CustomerBase):
    """Public view of Customer model."""

    pass
