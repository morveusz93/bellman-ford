from graph import Graph, Vertex

class BellmanFord:
    def __init__(self, graph) -> None:
        self.graph: Graph = graph

    def calculate(self, start_vertex: Vertex) -> None:
        start_vertex.set_distance(0)

        for _ in range(len(self.graph.vertices) - 1):
            for vertex in self.graph.vertices:
                for edge in self.graph.get_vertex_edges(vertex):
                    if edge.start_vertex.distance != float('inf') and edge.start_vertex.distance + edge.weight < edge.end_vertex.distance:
                        new_distance = edge.start_vertex.distance + edge.weight
                        edge.end_vertex.set_distance(new_distance)
        for vertex in self.graph.vertices:
            for edge in self.graph.get_vertex_edges(vertex):
                if edge.start_vertex.distance != float('inf') and edge.start_vertex.distance + edge.weight < edge.end_vertex.distance:
                    raise ValueError("Graf zawiera ujemny cykl")
