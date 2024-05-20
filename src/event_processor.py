import asyncio

from datetime import datetime, timedelta

from asyncio import Queue
from src.db.crud import update_order_status_in_db
from src.db.database import get_db_session
import logging

logger = logging.getLogger(__name__)


class MockOrderExecutor:
    ORDER_TIME = 5

    def __init__(self, queue: Queue):
        self.event_queue = queue

    async def event_worker(self):
        while True:
            if not self.event_queue.empty():
                event = await self.event_queue.get()
                current_time = datetime.now()
                logger.info(event)

                if current_time >= event.timestamp + timedelta(seconds=self.ORDER_TIME):

                    db = await get_db_session()
                    try:
                        await update_order_status_in_db(db, event.order_id, "executed")
                        logger.info(f"Order with ID {event.order_id} has been executed")
                    finally:
                        await db.close()
                else:
                    await self.event_queue.put(event)
                    await asyncio.sleep(1)
            else:
                await asyncio.sleep(1)
