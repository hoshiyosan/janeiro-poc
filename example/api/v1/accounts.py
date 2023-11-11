import asyncio
import logging

from fastapi import APIRouter
from pydantic import BaseModel

from example.domain.accounts.entity import AccountEntity

router = APIRouter(tags=["accounts"])
logger = logging.getLogger(__name__)


class AccountReadDTO(BaseModel):
    uuid: str
    username: str
    email: str


@router.post("/accounts", response_model=AccountReadDTO)
async def create_account():
    return AccountEntity.create({"username": "toto", "email": "toto@example.com"})
