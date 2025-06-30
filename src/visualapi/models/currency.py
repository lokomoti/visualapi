from sqlmodel import Field, SQLModel

import models


class CurrencyBase(SQLModel, table=True):
    __tablename__ = models.TABLE_NAME_CURRENCY
    __table_args__ = models.TABLE_ARGS

    rowid: int
    id: str = Field(primary_key=True)
    name: str | None
