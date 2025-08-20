from pathlib import Path

import util
from auth import signedurl
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi_cache.decorator import cache
from loguru import logger
from models.part import Part
from sqlmodel import Session, select
from api.deps import SessionDep, authorize

router = APIRouter(prefix="/{part_id}/drawing")


def get_part_drawing_path(part_id: str, session: Session) -> str | None:
    """Get the Visual file path of the part's drawing."""
    with session as session:
        statement = select(Part).where(Part.id == part_id)
        result = session.scalars(statement).one_or_none()

    if not result:
        raise ValueError(f"Part {part_id} not found")
    if not result.drawing_file:
        raise ValueError(f"Part {part_id} does not have a drawing file")


def retrieve_pdf(visual_file_path: str) -> FileResponse:
    """Retrieve the PDF file for the given visual file path."""
    mapped_path = Path(util.map_network_to_local(visual_file_path))

    logger.debug(f"Mapped drawing path: {mapped_path}")

    if not mapped_path.exists():
        raise HTTPException(status_code=404, detail="PDF file not found")

    return FileResponse(mapped_path, media_type="application/pdf")


@router.get("/", dependencies=[Depends(authorize)])
@cache(expire=60)
def get_drawing(part_id: str, db_session: SessionDep):
    """Get the drawing of a part by its ID."""
    with db_session as session:
        try:
            drawing_path = get_part_drawing_path(part_id, session)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    return retrieve_pdf(drawing_path)


@router.get("/signed/url", dependencies=[Depends(authorize)])
def get_signed_drawing(part_id: str, db_session: SessionDep):
    """Get a signed URL for the drawing of a part by its ID."""
    with db_session as session:
        try:
            get_part_drawing_path(part_id, session)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    return signedurl.create_signed_url(resource=f"drawing/{part_id}")


@router.get("/signed")
def get_signed_drawing_url(
    part_id: str, db_session: SessionDep, token=Query(...)
):
    """Get drawing using the signed URL."""
    try:
        signedurl.verify_signed_url(token=token, resource=f"drawing/{part_id}")
    except signedurl.SignedUrlError as e:
        raise HTTPException(status_code=403, detail=str(e))

    logger.debug(f"Successfully verified signed URL for drawing/{part_id}")

    with db_session as session:
        try:
            drawing_path = get_part_drawing_path(part_id, session)
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

    return retrieve_pdf(drawing_path)
