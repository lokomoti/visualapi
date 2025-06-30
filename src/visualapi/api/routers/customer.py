from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlmodel import Session, select

from db import get_db
from models.customer import Customer, CustomerPublic

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/", response_model=list[CustomerPublic])
@cache(expire=60)
def get_customers(
    customer_id: str | None = None,
    country_id: str | None = None,
    db_session: Session = Depends(get_db),
):
    """Get customers."""
    with db_session as session:
        statement = select(Customer)
        if customer_id:
            statement = statement.where(Customer.id == customer_id)
        if country_id:
            statement = statement.where(Customer.country_id == country_id)
        return session.scalars(statement).all()
