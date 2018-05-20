import heapq
import sys
class Graph:

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, name, edges):
        self.vertices[name] = edges # edges (long , direction)

    def shortest_path(self, start, finish):
        distances = {}  # Distance from start to node
        previous = {}  # Previous node in optimal path from source
        nodes = []  # Priority queue of all nodes in Graph

        for vertex in self.vertices:
            if vertex == start:  # Set root node as distance of 0
                distances[vertex] = 0
                heapq.heappush(nodes, [0, vertex])
            else:
                distances[vertex] = sys.maxsize
                heapq.heappush(nodes, [sys.maxsize, vertex])
            previous[vertex] = None

        while nodes:
            smallest = heapq.heappop(nodes)[1]  # Vertex in nodes with smallest distance in distances
            if smallest == finish:  # If the closest node is our target we're done so print the path
                path = []
                while previous[smallest]:  # Traverse through nodes til we reach the root which is 0
                    path.append(smallest)
                    smallest = previous[smallest]
                return path
            if distances[smallest] == sys.maxsize:  # All remaining vertices are inaccessible from source
                break

            for neighbor in self.vertices[smallest]:  # Look at all the nodes that this vertex is attached to
                alt = distances[smallest] + self.vertices[smallest][neighbor][0]  # Alternative path distance
                if alt < distances[neighbor]:  # If there is a new shortest path update our priority queue (relax)
                    distances[neighbor] = alt
                    previous[neighbor] = smallest
                    for n in nodes:
                        if n[1] == neighbor:
                            n[0] = alt
                            break
                    heapq.heapify(nodes)
        return distances

    def get_vertices_information(self,key):
        return self.vertices[key]
    def get_vertices_name(self):
        return self.vertices.keys()
    def __str__(self):
        return str(self.vertices)
    def __len__(self):
        return len(list(self.vertices.values()))

if __name__ =="__main__":
    g = Graph()
    g.add_vertex('A', {'B': (7, 60), 'C': (8, 60)})
    g.add_vertex('B', {'A': (7, 60), 'F': (2, 60)})
    g.add_vertex('C', {'A': (8, 60), 'F': (6, 60), 'G': (4, 60)})
    g.add_vertex('D', {'F': (8, 60)})
    g.add_vertex('E', {'H': (1, 60)})
    g.add_vertex('F', {'B': (2, 60), 'C': (6, 20), 'D': (8, 20), 'G': (9, 20), 'H': (3, 20)})
    g.add_vertex('G', {'C': (4, 20), 'F': (9, 20)})
    g.add_vertex('H', {'E': (1, 30), 'F': (3, 360)})
    print(g.shortest_path('A', 'H'))
    print(g.get_vertices_name())