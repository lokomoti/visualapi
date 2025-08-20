from fastapi import APIRouter
from fastapi_cache.decorator import cache
from models.customer import Customer, CustomerPublic
from sqlmodel import select

from api.deps import SessionDep

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/", response_model=list[CustomerPublic])
@cache(expire=60)
def get_customers(
    session: SessionDep,
    customer_id: str | None = None,
    country_id: str | None = None,
):
    """Get customers."""
    statement = select(Customer)
    if customer_id:
        statement = statement.where(Customer.id == customer_id)
    if country_id:
        statement = statement.where(Customer.country_id == country_id)
    return session.scalars(statement).all()
