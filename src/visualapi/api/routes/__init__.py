"""API Routers for Visual API"""

from fastapi import APIRouter, Depends

from api.deps import authorize
from api.routes.customer import router as customer_router
from api.routes.customerorder import router as customerorder_router
from api.routes.customerorderline import router as customerorderline_router
from api.routes.part import router as part_router
from api.routes.workorder import router as workorder_router
from api.routes.health import router as health_router

router = APIRouter(prefix="/api")

router.include_router(workorder_router, dependencies=[Depends(authorize)])
router.include_router(part_router)  # Exluded auth for allowing signed url endpoints
router.include_router(customerorder_router, dependencies=[Depends(authorize)])
router.include_router(customerorderline_router, dependencies=[Depends(authorize)])
router.include_router(customer_router, dependencies=[Depends(authorize)])
router.include_router(health_router)
