# Nombre: Maylon Javier Polanco
# Matrícula: 15-EISN-2-004

class Node:
    def run(self, boss, player):
        raise NotImplementedError

class Selector(Node):
    def __init__(self, children):
        self.children = children

    def run(self, boss, player):
        for child in self.children:
            if child.run(boss, player):
                return True
        return False

class Sequence(Node):
    def __init__(self, children):
        self.children = children

    def run(self, boss, player):
        for child in self.children:
            if not child.run(boss, player):
                return False
        return True

class Condition(Node):
    def __init__(self, condition_func):
        self.condition_func = condition_func

    def run(self, boss, player):
        return self.condition_func(boss, player)

class Action(Node):
    def __init__(self, action_func):
        self.action_func = action_func

    def run(self, boss, player):
        self.action_func(boss, player)
        return True
