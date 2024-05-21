from dataclasses import dataclass
from datetime import datetime


@dataclass
class OrderEvent:
    order_id: str
    timestamp: datetime
