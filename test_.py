from graph import Graph, Node
import random

def test_create_graph_with_empty_node_list():
    graph = Graph()
    assert graph.nodes == []

def test_created_node_has_correct_position():
    x = random.randint(0, 1000)
    y = random.randint(0, 1000)
    pos = (x,y)

    node = Node(pos)

    assert node.pos == pos

def test_created_node_by_graph_object_has_coorect_position():
    x = random.randint(0, 1000)
    y = random.randint(0, 1000)
    pos = (x,y)

    graph = Graph()
    graph.create_node(pos)

    assert graph.nodes[0].pos == pos

def test_node_init_active_is_false():
    node = _create_node()
    
    assert node.active is False

def test_node_toggle_active():
    node = _create_node()
    node.toggle_active()
    assert node.active is True


def _create_node():
    x = random.randint(0, 1000)
    y = random.randint(0, 1000)
    pos = (x,y)

    node = Node(pos)
    return node