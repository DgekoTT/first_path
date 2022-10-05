import math


class Vertex:
    def __init__(self):
        self._links = []

    @property
    def links(self):
        return self._links


class Link:
    def __init__(self, v1, v2):
        self._v1 = v1
        self._v2 = v2
        self._dist = 1

    @property
    def v1(self):
        return self._v1

    @property
    def v2(self):
        return self._v2

    @property
    def dist(self):
        return self._dist

    @dist.setter
    def dist(self, new):
        if type(new) not in (int, float):
            raise TypeError('wrong type of change')
        self._dist = new


class LinkedGraph:
    def __init__(self):
        self._links = []
        self._vertex = []
        self.spy_vertex = {}

    @property
    def links(self):
        return self._links

    def add_vertex(self, v):
        if v in self._vertex:
            return
        self._vertex.append(v)

    def add_link(self, link):
        for i in self.links:
            if set([i.v1, i.v2]) == set([link.v1, link.v2]):
                return
        self._links.append(link)
        first_vertex = link.v1
        second_vertex = link.v2
        if link not in first_vertex._links:
            first_vertex._links.append(link)
        if link not in second_vertex._links:
            second_vertex._links.append(link)
        self.add_vertex(first_vertex)
        self.add_vertex(second_vertex)

    def matrix_smegnost(self, start_v):
        a = len(self._vertex) + 1
        matrix_start_v = [[math.inf for _ in range(a)] for _ in range(a)]
        name_vertex = [0,]
        name_vertex.append(start_v)

        for i in self._vertex:# создал название столбцов смежной матрицы
            if i is not start_v:
                name_vertex.append(i)
        matrix_start_v[0] = name_vertex

        for g in range(a):
            matrix_start_v[g][0] = name_vertex[g]

        spy_vertex = self.spy_vertex
        for k, i in enumerate(name_vertex):
            spy_vertex[i] = k

        for i in range(1, len(name_vertex)):
            for link in name_vertex[i].links:
                if link.v1 == name_vertex[i]:
                    matrix_start_v[spy_vertex[name_vertex[i]]][spy_vertex[link.v2]] = link.dist
                if link.v2 == name_vertex[i]:
                    matrix_start_v[spy_vertex[name_vertex[i]]][spy_vertex[link.v1]] = link.dist
        for i in range(len(matrix_start_v)):
            matrix_start_v[i][i] = 0
        new_matrix = matrix_start_v[1:]
        for i in new_matrix:
           i.pop(0)

        self.spy_vertex = spy_vertex
        return new_matrix

    def find_path(self, start_v, stop_v):
        V = self.matrix_smegnost(start_v)

        def get_path(P, u, v):
            path = [u]
            while u != v:
                u = P[u][v]
                path.append(u)

            return path


        N = len(V)  # число вершин в графе
        P = [[v for v in range(N)] for u in
             range(N)]  # начальный список предыдущих вершин для поиска кратчайших маршрутов

        for k in range(N):
            for i in range(N):
                for j in range(N):
                    d = V[i][k] + V[k][j]
                    if V[i][j] > d:
                        V[i][j] = d
                        P[i][j] = k  # номер промежуточной вершины при движении от i к j

        # нумерацця вершин начинается с нуля
        start = self.spy_vertex[start_v] - 1
        end = self.spy_vertex[stop_v] - 1
        stations = [i + 1 for i in get_path(P, end, start)[::-1]]
        find_stations = {}
        for key, values in self.spy_vertex.items():
            find_stations[values] = key
        name_stations = [find_stations[i] for i in stations]
        link_path = []
        for i in range(len(name_stations) - 1):
            for link in name_stations[i].links:
                if name_stations[i] in (link.v1, link.v2) and name_stations[i + 1] in (link.v1, link.v2):
                    link_path.append(link)
        return (name_stations, link_path)


class Station(Vertex):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class LinkMetro(Link):
    def __init__(self, v1, v2, dist):
        if type(dist) not in (int, float) or dist < 0:
            raise TypeError('wrong type and dist must be > 0')
        super().__init__(v1, v2)
        self._dist = dist


map_metro = LinkedGraph()
s1 = Station("Первая конная")
s2 = Station("Майская")
s3 = Station("Глубокое озеро")
s4 = Station("7 домов")
s5 = Station("Кузнецкий молот")
s6 = Station("Снежная")
s7 = Station("Верхняя 2")

map_metro.add_link(LinkMetro(s1, s2, 1))
map_metro.add_link(LinkMetro(s2, s3, 1))
map_metro.add_link(LinkMetro(s1, s3, 1))

map_metro.add_link(LinkMetro(s4, s5, 1))
map_metro.add_link(LinkMetro(s6, s7, 1))

map_metro.add_link(LinkMetro(s2, s7, 5))
map_metro.add_link(LinkMetro(s3, s4, 3))
map_metro.add_link(LinkMetro(s5, s6, 3))

print(f' Количество путей {len(map_metro._links)}')
print(f" Количество станций {len(map_metro._vertex)}")
start, end = s1, s6
path = map_metro.find_path(start, end)
print(f'Начало маршрута {start}')
print(f'Станции маршрута {path[0]}')
print(f'Конец маршрута {end}')
print(f"Длина маршрута {sum([x.dist for x in path[1]])}")
