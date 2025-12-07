import heapq
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from collections import deque

@dataclass(order=True)
class Event:
    time:float
    priority: int
    type: str= field(compare=False)
    customer_id: int= field(compare=False)
    server_id: Optional[int]= field(default=None, compare=False)
    

class Server:
    def __init__(self, server_id):
      self.id = server_id
      self.coada = deque()
      self.ocupat = False
      self.client_curent = None
      self.start_service_time = {}
    
    def adauga_client(self,client_id):
        self.coada.append(client_id)

    
    def poate_incepe_serviciul(self):
        return (not self.ocupat) and (len(self.coada) > 0) 
    
    def incepe_serviciul(self, current_time):
        client_id = self.coada.popleft()
        self.client_curent = client_id
        self.ocupat = True
        self.start_service_time[client_id] = current_time
        return client_id
    
    def termina_serviciul(self):
        self.ocupat = False
        self.client_curent = None
        
    
    def genereaza_servicu_si_plecare(server_id, client_id, current_time, service_rate):
        durata_serviciu = random.expovariate(service_rate)
        departure_time = current_time + durata_serviciu

        eveniment_plecare = Event(
            time = departure_time,
            priority = 1,
            type = "departure",
            customer_id = client_id,
            server_id = server_id
        )
        return eveniment_plecare