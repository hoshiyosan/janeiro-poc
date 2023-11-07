from fastapi import APIRouter
import logging
import asyncio

router = APIRouter(tags=["accounts"])
logger = logging.getLogger(__name__)

@router.post("/accounts")
async def create_account():
    logger.info("Creating account")
    await asyncio.sleep(1)
    logger.info("Account created")
