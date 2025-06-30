from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlmodel import Session, select

from db import get_db
from models.part import Part, PartPublic

router = APIRouter()


@router.get(
    "/{part_id}",
    response_model=PartPublic,
    responses={404: {"description": "Part not found"}},
)
@cache(expire=60)
def get_part(part_id: str, db_session: Session = Depends(get_db)):
    """Get a part by its ID."""
    with db_session as session:
        statement = select(Part).where(Part.id == part_id)
        result = session.scalars(statement)
        part = result.one_or_none()

        if not part:
            raise HTTPException(status_code=404, detail=f"Part '{part_id}' not found")

        return part


@router.get(
    "/",
    response_model=list[PartPublic],
)
@cache(expire=60)
def get_parts(
    part_id_startswith: str | None,
    exclude_obsolete: bool = True,
    db_session: Session = Depends(get_db),
):
    """Get parts, optionally filtered by ID prefix and obsolete status."""
    with db_session as session:
        statement = select(Part)

        if part_id_startswith:
            statement = statement.where(Part.id.startswith(part_id_startswith))

        if exclude_obsolete:
            statement = statement.where(Part.obsolete is not True)

        result = session.scalars(statement)
        parts = result.all()

        return parts
