from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models import Order


async def get_orders(db: AsyncSession):
    result = await db.execute(select(Order))
    return result.scalars().all()


async def create_order(db: AsyncSession, order: Order):
    db.add(order)
    await db.commit()
    await db.refresh(order)
    return order


async def get_order(db: AsyncSession, order_id: str):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    return result.scalars().first()


async def delete_order(db: AsyncSession, order: Order):
    await db.delete(order)
    await db.commit()
