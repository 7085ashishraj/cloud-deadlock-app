import networkx as nx
from typing import List, Dict, Tuple

class DeadlockDetector:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_process(self, process_id: str):
        self.graph.add_node(process_id, type='process')

    def add_resource(self, resource_id: str):
        self.graph.add_node(resource_id, type='resource')

    def request_resource(self, process_id: str, resource_id: str):
        # Edge from Process to Resource indicates a Request
        self.graph.add_edge(process_id, resource_id)

    def allocate_resource(self, process_id: str, resource_id: str):
        # Edge from Resource to Process indicates an Allocation
        self.graph.add_edge(resource_id, process_id)

    def detect_deadlock(self) -> Dict:
        """
        Detects cycles in the Resource Allocation Graph.
        Returns a dictionary with 'has_deadlock' standard boolean and 'cycles' list if present.
        """
        cycles = list(nx.simple_cycles(self.graph))
        return {
            "has_deadlock": len(cycles) > 0,
            "cycles": cycles
        }
    
    def clear(self):
        self.graph.clear()
