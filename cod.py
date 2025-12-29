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
        
    
    def genereaza_serviciu_si_plecare(server_id, client_id, current_time, service_rate):
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
    
    class Simulator:
        def __init__(self, num_servers, arrival_rate, service_rate, max_time):
            self.arrival_rate = arrival_rate
            self.service_rate = service_rate
            self.max_time = max_time
            self.current_time = 0.0
            self.event_queue: List[Event] = []
            heapq.heapify(self.event_queue)
            self.servers = [Server(i) for i in range(num_servers)]
            self.next_customer_id = 0
            self.wait_times = []

        def initializeaza(self):
            timp_sosire = random.expovariate(self.arrival_rate)
            eveniment_sosire = Event(
                time=timp_sosire,
                priority=0,
                type="arrival",
                customer_id=self.next_customer_id
            )
            heapq.heappush(self.event_queue, eveniment_sosire)
            self.next_customer_id += 1

        def gaseste_server_liber(self):
            for server in self.servers:
                if not server.ocupat:
                    return server
                return None
            
        def proceseaza_sosire(self, event: Event):
            self.current_time = event.time
            client_id = event.customer_id

            server = self.gaseste_server_liber()
            if server:
                server.adauga_client(client_id)
                client_servit = server.incepe_serviciul(self.current_time)

                eveniment_plecare = server.genereaza_serviciu_si_plecare(
                    server.id,
                    client_servit,
                    self.current_time,
                    self.service_rate
                )

                heapq.heappush(self.event_queue, eveniment_plecare)
            else:
                self.servers[0].adauga_client(client_id)

        def proceseaza_plecare(self, event: Event):
            self.current_time = event.time
            server = self.servers[event.server_id]
            client_id = event.customer_id

            start_time = server.start_service_time[client_id]
            timp_asteptare = start_time
            self.wait_times.append(timp_asteptare)

            server.termina_serviciul()

            if server.coada:
                client_nou = server.incepe_serviciul(self.current_time)

                eveniment_plecare = server.genereaza_serviciu_si_plecare(
                    server.id,
                    client_nou,
                    self.current_time,
                    self.service_rate
                )

                heapq.heappush(self.event_queue, eveniment_plecare)
                