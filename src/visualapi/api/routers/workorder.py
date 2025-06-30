from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_cache.decorator import cache
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from db import get_db
from models.workorder import WorkOrder, WorkOrderPublic, WorkOrderStatus

router = APIRouter(prefix="/workorders", tags=["Workorders"])


@router.get(
    "/{base_id}",
    response_model=WorkOrderPublic,
    responses={404: {"description": "Work order not found"}},
)
@cache(expire=60)
def get_workorder(base_id: str, db_session: Session = Depends(get_db)):
    """Get a work order by its base ID."""
    with db_session as session:
        statement = (
            select(WorkOrder)
            .where(WorkOrder.base_id == base_id)
            .options(selectinload(WorkOrder.part))
        )
        result = session.scalars(statement)
        work_order = result.one_or_none()

        if not work_order:
            raise HTTPException(
                status_code=404, detail=f"Work order '{base_id}' not found"
            )

        return work_order


@router.get(
    "/",
    response_model=list[WorkOrderPublic],
)
@cache(expire=60)
def get_workorders(
    status: list[WorkOrderStatus] = Query(
        default=None, description="List of status chars"
    ),
    base_id_startswith: str | None = None,
    db_session: Session = Depends(get_db),
):
    """Get all work orders, optionally filtered by statuses or base ID."""
    with db_session as session:
        statement = select(WorkOrder).options(selectinload(WorkOrder.part))

        if status:
            statement = statement.where(WorkOrder.status.in_(s.value for s in status))
        if base_id_startswith:
            statement = statement.where(
                WorkOrder.base_id.startswith(base_id_startswith)
            )

        result = session.scalars(statement)
        work_orders = result.all()

        return work_orders
