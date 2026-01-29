# Clase grafo, operaciones con grafos
import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Optional

class SocialGraph:
    def __init__(self):
        self.graph = nx.Graph()

    def add_user(self, username: str):
        """Agrega un nodo (usuario) al grafo"""
        if username not in self.graph:
            self.graph.add_node(username)
            return True
        return False
    
    def add_friendship(self, user1: str, user2: str):
        """Agrega una arista (amistad) bidireccional"""
        if user1 in self.graph and user2 in self.graph:
            self.graph.add_edge(user1, user2)
            return True
        return False
    
    def remove_friendship(self, user1: str, user2: str):
        """Elimina una arista (amistad) bidireccional"""
        if self.graph.has_edge(user1, user2):
            self.graph.remove_edge(user1, user2)
            return True
        return False
    
    def get_friends(self, username: str) -> List[str]:
        """Retorna lista de amigos de un usuario"""
        return list(self.graph.neighbors(username))
    
    def find_friend_path(self, start: str, end: str) -> Optional[List[str]]:
        """Busca un camino entre dos usuarios usando BFS"""
        try:
            return nx.shortest_path(self.graph, source=start, target=end)
        
        except nx.NetworkXNoPath:
            return None
        
    def get_statistics(self) -> dict:
        """Calcula estadísticas del grafo"""
        if self.graph.number_of_nodes() == 0:
            return {"max": (None, 0), "min": (None, 0), "avg": 0}
        
        # Grados de cada nodo
        degrees = dict(self.graph.degree())
        max_user = max(degrees, key=degrees.get)
        min_user = min(degrees, key=degrees.get)
        avg = sum(degrees.values()) / len(degrees)

        return {
            "max": (max_user, degrees[max_user]),
            "min": (min_user, degrees[min_user]),
            "avg": avg
        }
    
    def draw_graph(self):
        """Dibuja el grafo usando NetworkX/Matplotlib"""
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(self.graph, seed=42)
        nx.draw(
            self.graph, pos,
            with_labels=True,
            node_color='lightblue',
            node_size=1500,
            font_size=10,
            edge_color='gray'
        )
        plt.title("Red Social - SocialTEC")
        plt.show()