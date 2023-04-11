from graph import Graph, Vertex
import random

def test_create_graph_with_empty_vertex_list():
    graph = Graph()
    assert graph.vertices == []

def test_created_vertex_has_correct_position():
    x = random.randint(0, 1000)
    y = random.randint(0, 1000)
    pos = (x,y)

    vertex = Vertex(pos)

    assert vertex.pos == pos

def test_created_vertex_by_graph_object_has_coorect_position():
    x = random.randint(0, 1000)
    y = random.randint(0, 1000)
    pos = (x,y)

    graph = Graph()
    graph.create_vertex(pos)

    assert graph.vertices[0].pos == pos

def test_vertex_init_active_is_false():
    vertex = _create_vertex()
    
    assert vertex.active is False

def test_vertex_toggle_active():
    vertex = _create_vertex()
    vertex.toggle_active()
    assert vertex.active is True


def _create_vertex():
    x = random.randint(0, 1000)
    y = random.randint(0, 1000)
    pos = (x,y)

    vertex = Vertex(pos)
    return vertex