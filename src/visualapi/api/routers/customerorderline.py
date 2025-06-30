from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from db import get_db
from models.customerorderline import (CustomerOrderLine,
                                      CustomerOrderLinePublic,
                                      CustomerOrderLineWithPartPublic)

router = APIRouter(prefix="/customerorderlines", tags=["Customer Order Lines"])


@router.get(
    "/{customer_order_id}/{line_no}",
    response_model=CustomerOrderLineWithPartPublic,
    responses={404: {"description": "Customer order line not found"}},
)
@cache(expire=60)
def get_customer_order_line(
    customer_order_id: str, line_no: int, db_session: Session = Depends(get_db)
) -> CustomerOrderLineWithPartPublic:
    """Get customer order line by ID and line number."""
    with db_session as session:
        statement = (
            select(CustomerOrderLine)
            .where(
                CustomerOrderLine.cust_order_id == customer_order_id,
                CustomerOrderLine.line_no == line_no,
            )
            .options(selectinload(CustomerOrderLine.part))
        )

        result = session.scalars(statement).one_or_none()
        if not result:
            raise HTTPException(status_code=404, detail="Customer order line not found")

        return result


@router.get("/{customer_order_id}", response_model=list[CustomerOrderLinePublic])
@cache(expire=60)
def get_customer_order_lines(
    customer_order_id: str, db_session: Session = Depends(get_db)
) -> list[CustomerOrderLinePublic]:
    """Get all customer order lines for a given customer order ID."""
    with db_session as session:
        statement = (
            select(CustomerOrderLine)
            .where(CustomerOrderLine.cust_order_id == customer_order_id)
            .options(selectinload(CustomerOrderLine.part))
        )

        results = session.scalars(statement).all()

        return results
