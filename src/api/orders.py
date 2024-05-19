import random

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from asyncio import sleep
from src.api import schemes
from src.db import crud
from src.db.database import get_db
from src.db.models import Order
from typing import List
from src.core.log_config import setup_logger
from logging import getLogger

setup_logger()
logger = getLogger(__name__)

router = APIRouter()


async def delay():
    delay_time = random.random()
    delay_time = 0.1 if delay_time < 0.1 else delay_time
    logger.info(f"Delay time is {delay_time}")
    await sleep(delay_time)


@router.get(
    "/",
    response_model=List[schemes.OrderOutput],
    summary="Retrieve all orders",
    operation_id="getOrders",
)
async def get_orders(db: AsyncSession = Depends(get_db)):
    await delay()
    return await crud.get_orders(db)


@router.post(
    "/",
    response_model=schemes.OrderOutput,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": schemes.Error}},
    summary="Place a new order",
    operation_id="placeOrder",
)
async def place_order(order: schemes.OrderInput, db: AsyncSession = Depends(get_db)):
    await delay()
    db_order = Order(**order.dict())
    return await crud.create_order(db, db_order)


@router.get(
    "/{order_id}",
    response_model=schemes.OrderOutput,
    summary="Retrieve a specific order",
    operation_id="getOrder",
    responses={404: {"model": schemes.Error}},
)
async def get_order(order_id: str, db: AsyncSession = Depends(get_db)):
    await delay()
    order = await crud.get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancel an order",
    operation_id="cancelOrder",
    responses={404: {"model": schemes.Error}},
)
async def cancel_order(order_id: str, db: AsyncSession = Depends(get_db)):
    await delay()
    order = await crud.get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    await crud.delete_order(db, order)
    logger.info(order)
    return order
