# scripts/behavior_tree.py


class NodeStatus:
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RUNNING = "RUNNING"

class Node:
    def tick(self, agent):
        raise NotImplementedError

# Secuencia: todos deben tener éxito para continuar
class Sequence(Node):
    def __init__(self, children):
        self.children = children

    def tick(self, agent):
        for child in self.children:
            result = child.tick(agent)
            if result != NodeStatus.SUCCESS:
                return result
        return NodeStatus.SUCCESS

# Selector: ejecuta el primero que funcione
class Selector(Node):
    def __init__(self, children):
        self.children = children

    def tick(self, agent):
        for child in self.children:
            result = child.tick(agent)
            if result == NodeStatus.SUCCESS:
                return NodeStatus.SUCCESS
        return NodeStatus.FAILURE

# Hoja (acción): recibe una función personalizada
class Action(Node):
    def __init__(self, function):
        self.function = function

    def tick(self, agent):
        return self.function(agent)
