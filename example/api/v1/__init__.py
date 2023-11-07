from fastapi import APIRouter

from . import accounts

router = APIRouter(prefix="/v1")

router.include_router(accounts.router)
