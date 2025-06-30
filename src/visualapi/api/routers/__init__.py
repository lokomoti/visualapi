"""API Routers for Visual API"""

from fastapi import APIRouter, Depends

from api.routers.customer import router as customer_router
from api.routers.customerorder import router as customerorder_router
from api.routers.customerorderline import router as customerorderline_router
from api.routers.part import router as part_router
from api.routers.workorder import router as workorder_router
from auth import api

router = APIRouter(prefix="/api", dependencies=[Depends(api.authorize)])

router.include_router(workorder_router)
router.include_router(part_router)
router.include_router(customerorder_router)
router.include_router(customerorderline_router)
router.include_router(customer_router)
