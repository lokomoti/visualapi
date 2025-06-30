from fastapi import APIRouter

from api.routers.part.drawing import router as drawing_router
from api.routers.part.part import router as parts_router

router = APIRouter(prefix="/parts", tags=["Parts"])

router.include_router(parts_router)
router.include_router(drawing_router)
