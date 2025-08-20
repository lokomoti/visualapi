from fastapi import APIRouter, Depends

from api.deps import authorize
from api.routes.part.drawing import router as drawing_router
from api.routes.part.part import router as parts_router

router = APIRouter(prefix="/parts", tags=["Parts"])

router.include_router(parts_router, dependencies=[Depends(authorize)])
router.include_router(drawing_router)
