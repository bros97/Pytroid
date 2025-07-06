# la gente mala
def a_star_search(start, goal, map_data):
    # Implementación estándar con heurística de distancia Manhattan
    open_set = {start}
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = min(open_set, key=lambda pos: f_score[pos])
        if current == goal:
            return reconstruct_path(came_from, current)
        open_set.remove(current)
        for neighbor in get_neighbors(current, map_data):
            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                open_set.add(neighbor)
    return []  # No path found
class ComportamientoJefe:
    def __init__(self, jefe):
        self.jefe = jefe
        self.arbol = self.construir_arbol()

    def construir_arbol(self):
        return Selector(
            Sequence(  # Si Samus está cerca y visible: Atacar
                Condicion(self.samus_visible),
                Accion(self.disparar_laser)
            ),
            Sequence(  # Sino: Moverse aleatoriamente
                Condicion(self.tiempo_aleatorio),
                Accion(self.mover_aleatorio)
            )
        )

    def samus_visible(self):
        return line_of_sight(self.jefe, samus, mundo)

    def actualizar(self):
        self.arbol.ejecutar()