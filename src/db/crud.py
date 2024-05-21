from datetime import datetime

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Order
from src.api.ws.orders import manager
from logging import getLogger
from src.api.ws.schemes import OrderEvent
from asyncio import Queue


logger = getLogger(__name__)

event_queue: Queue[OrderEvent] = Queue()


async def get_orders_from_db(db: AsyncSession):
    result = await db.execute(select(Order))
    return result.scalars().all()


async def create_order_in_db(db: AsyncSession, order: Order):
    db.add(order)
    await db.commit()
    await db.refresh(order)
    await manager.broadcast(f"New order created: {order.__dict__}")
    await event_queue.put(OrderEvent(order.id, datetime.now()))
    return order


async def get_order_by_id(db: AsyncSession, order_id: str):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    return result.scalars().first()


async def delete_order_from_db(db: AsyncSession, order: Order):
    await db.delete(order)
    await db.commit()

    order_message = order.__dict__
    order_message.pop('_sa_instance_state')
    await manager.broadcast(f"Order deleted: {order.__dict__}")

    logger.info(f"Deleted order with ID: {order.id}")


async def update_order_status_in_db(db: AsyncSession, order_id: str, status: str):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    order = result.scalars().first()
    if order:
        order.status = status
        await db.commit()
        await manager.broadcast(f"Order status updated: {order.id} - {order.status}")
        logger.info(f"Updated order status: {order.id} - {order.status}")
        return order
    else:
        logger.warning(f"Order not found: {order_id}")
