from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from db import get_db
from models.customerorder import CustomerOrder, CustomerOrderPublic

router = APIRouter(prefix="/customerorders", tags=["Customer Orders"])


@router.get(
    "/{customer_order_id}",
    response_model=CustomerOrderPublic,
    responses={404: {"description": "Customer order not found"}},
)
@cache(expire=60)
def get_customer_order(
    customer_order_id: str,
    db_session: Session = Depends(get_db),
):
    """Get a customer order by ID."""
    with db_session as session:
        statement = (
            select(CustomerOrder)
            .where(CustomerOrder.id == customer_order_id)
            .options(
                selectinload(CustomerOrder.customer),
                selectinload(CustomerOrder.order_lines),
            )
        )

        result = session.scalars(statement).one_or_none()

        if not result:
            raise HTTPException(status_code=404, detail="Customer order not found")

        return result


@router.get(
    "/",
    response_model=list[CustomerOrderPublic],
)
@cache(expire=60)
def get_customer_orders(
    customer_id: str | None = None,
    order_id_startswith: str | None = None,
    db_session: Session = Depends(get_db),
):
    """Get all customer orders, optionally filtered by customer ID or order ID prefix."""
    with db_session as session:
        statement = select(CustomerOrder).options(
            selectinload(CustomerOrder.customer),
            selectinload(CustomerOrder.order_lines),
        )

        if customer_id:
            statement = statement.where(CustomerOrder.customer_id == customer_id)

        if order_id_startswith:
            statement = statement.where(
                CustomerOrder.id.startswith(order_id_startswith)
            )

        results = session.scalars(statement).all()

        return results
