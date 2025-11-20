import heapq
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass(order=True)
class Event:
    time:float
    priority: int
    type: str= field(compare=False)
    customer_id: int= field(compare=False)
    server_id: Optional[int]= field(default=None, compare=False)
    

