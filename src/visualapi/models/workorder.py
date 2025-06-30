"""Workoder model for the visual API."""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

import models
from models.part import Part, PartPublic


class WorkOrderStatus(Enum):
    """Enumeration for work order status."""

    CLOSED = "C"  # Work order is completed
    FIRMED = "F"  # Engineering is complete. Date and quantities are firm.
    RELEASED = "R"  # Work is authorized to start based on the specified release date.
    UNRELASED = "U"  # Engineering is in process or dates and quantities are not firm.
    CANCELLED = "X"  # Work order will not be started or completed


class WorkOrderBase(SQLModel):
    """Base model for WorkOrder."""

    type: str = Field(primary_key=True, max_length=1)
    base_id: str = Field(primary_key=True, max_length=30)
    lot_id: str = Field(primary_key=True, max_length=3)
    split_id: str = Field(primary_key=True, max_length=3)
    sub_id: str = Field(primary_key=True, max_length=3)
    desired_qty: float | None
    received_qty: float | None
    create_date: datetime | None
    status: str


class WorkOrder(WorkOrderBase, table=True):
    """WorkOrder model."""

    __tablename__ = models.TABLE_NAME_WORK_ORDER
    __table_args__ = models.TABLE_ARGS

    rowid: int
    part_id: str | None = Field(
        foreign_key=f"{models.SCHEMA}.{models.TABLE_NAME_PART}.id", max_length=30
    )
    part: Optional[Part] = Relationship()


class WorkOrderPublic(WorkOrderBase):
    """Public model for WorkOrder."""

    part: Optional[PartPublic] = None
    status: WorkOrderStatus
