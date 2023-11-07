from fastapi import APIRouter

from . import v1 as api_v1

router = APIRouter()

router.include_router(api_v1.router)
