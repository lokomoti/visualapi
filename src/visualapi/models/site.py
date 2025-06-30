"""Site model."""

from sqlmodel import Field, SQLModel

import models


class Site(SQLModel, table=True):
    """Site model."""

    __tablename__ = models.TABLE_NAME_SITE
    __table_args__ = models.TABLE_ARGS

    rowid: int
    id: str = Field(primary_key=True)
    entity_id: str
    site_name: str | None
    site_addr_1: str | None
    site_addr_2: str | None
    site_addr_3: str | None
    site_zipcode: str | None
    site_country: str | None
    status: str | None
