from fastapi import APIRouter
import logging
import asyncio
from example.domain.accounts.entity import AccountEntity
from pydantic import BaseModel

router = APIRouter(tags=["accounts"])
logger = logging.getLogger(__name__)

class AccountReadDTO(BaseModel):
    uuid: str
    username: str
    email: str

@router.post("/accounts", response_model=AccountReadDTO)
async def create_account():
    return AccountEntity.create({"username": "toto", "email": "toto@example.com"})
