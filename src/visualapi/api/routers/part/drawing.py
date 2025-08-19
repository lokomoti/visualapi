from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi_cache.decorator import cache
from sqlmodel import Session, select
import util
from loguru import logger

from db import get_db
from models.part import Part

router = APIRouter(prefix="/{part_id}/drawing")


@router.get("/")
@cache(expire=60)
def get_drawing(part_id: str, db_session: Session = Depends(get_db)):
    """
    Get the drawing of a part by its ID.
    """
    with db_session as session:
        statement = select(Part).where(Part.id == part_id)
        result = session.scalars(statement).one_or_none()

    if not result:
        raise HTTPException(status_code=404, detail=f"Part {part_id} not found")

    if result.drawing_file:
        original_drawing_path = Path(result.drawing_file)
        mapped_drawing_path = util.map_network_to_local(original_drawing_path)

        logger.debug(f"Mapped drawing path for part {part_id}: {mapped_drawing_path}")

        if not mapped_drawing_path.exists():
            raise HTTPException(
                status_code=404, detail=f"Drawing file for part {part_id} not found"
            )

        return FileResponse(
            mapped_drawing_path, media_type="application/pdf", filename=mapped_drawing_path.name
        )

    else:
        raise HTTPException(
            status_code=404, detail=f"No drawing file associated with part {part_id}"
        )
