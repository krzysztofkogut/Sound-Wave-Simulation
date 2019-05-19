import sys

from numpy.core.umath import pi
from numpy.ma import sin

scale = 50  # 1m -> 50 cells
size_x = 6 * scale
size_y = 4 * scale
damping = 0.99
omega = 3 / (2 * pi)

initial_P = 200
vertPos = size_y - 2 * scale
horizPos = 3 * scale
wallTop = size_y - 3 * scale
wallTop1 = size_y - 1.5 * scale
wallTop2 = size_y - 2.5 * scale
wall_x_pos = 2 * scale
wall_x_pos1 = 2.5 * scale
wall_x_pos2 = 3.5 * scale
radius = 1 * scale
max_pressure = initial_P / 2
min_presure = -initial_P / 2

class Simulation2:
    def __init__(self):
        self.frame = 0
        self.scale = 50
        self.damping = 0.99
        self.vertPos1 = size_y - 2 * self.scale
        self.horizPos1 = 2 * self.scale
        self.vertPos2 = size_y - 2 * self.scale
        self.horizPos2 = 4 * self.scale
        self.pressure = [[0.0 for x in range(size_x)] for y in range(size_y)]
        self._velocities = [[[0.0, 0.0, 0.0, 0.0] for x in range(size_x)] for y in range(size_y)]
        self.pressure[self.vertPos1][self.horizPos1] = initial_P
        self.pressure[self.vertPos2][self.horizPos2] = initial_P

    def updateV(self):
        """Recalculate outflow velocities from every cell basing on preassure difference with each neighbour"""
        V = self._velocities
        P = self.pressure
        for i in range(size_y):
            for j in range(size_x):
                if wall[i][j] == 1:
                    V[i][j][0] = V[i][j][1] = V[i][j][2] = V[i][j][3] = 0.0
                    continue
                cell_pressure = P[i][j]
                V[i][j][0] = V[i][j][0] + cell_pressure - P[i - 1][j] if i > 0 else cell_pressure
                V[i][j][1] = V[i][j][1] + cell_pressure - P[i][j + 1] if j < size_x - 1 else cell_pressure
                V[i][j][2] = V[i][j][2] + cell_pressure - P[i + 1][j] if i < size_y - 1 else cell_pressure
                V[i][j][3] = V[i][j][3] + cell_pressure - P[i][j - 1] if j > 0 else cell_pressure

    def updateP(self):
        for i in range(size_y):
            for j in range(size_x):
                self.pressure[i][j] -= 0.5 * self.damping * sum(self._velocities[i][j])

    def step(self):
        self.pressure[self.vertPos1][self.horizPos1] = initial_P * sin(omega * self.frame)
        self.pressure[self.vertPos2][self.horizPos2] = initial_P * sin(omega * self.frame)
        self.updateV()
        self.updateP()
        self.frame += 1


argc = len(sys.argv)
if argc > 1 and sys.argv[1] == '1':
    wall = [[1 if x == wall_x_pos and wallTop < y < size_y else 0
             for x in range(size_x)] for y in range(size_y)]

elif argc > 1 and sys.argv[1] == '2':

    wall = [[1 if (x == wall_x_pos and wallTop + scale < y < size_y) or
                  (wall_x_pos - scale < x < wall_x_pos and
                   x - wall_x_pos == y - wallTop - scale - 1) or
                  (wall_x_pos < x < wall_x_pos + scale and
                   x - wall_x_pos == -y + wallTop + scale + 1)
             else 0
             for x in range(size_x)] for y in range(size_y)]

elif argc > 1 and sys.argv[1] == '3':
    wall = [[1 if (x == wall_x_pos and wallTop + scale < y < size_y) or
                  (wall_x_pos - scale < x < wall_x_pos and
                   x - wall_x_pos == y - wallTop - scale - 1) or
                  (wall_x_pos < x < wall_x_pos + scale and
                   x - wall_x_pos == -y + wallTop + scale + 1) or
                  (wall_x_pos - 0.75 * scale < x < wall_x_pos - scale / 2 and
                   x - wall_x_pos == -y + wallTop - scale / 2 + 1) or
                  (wall_x_pos + scale / 2 < x < wall_x_pos + 0.75 * scale and
                   x - wall_x_pos == y - wallTop + scale / 2 - 1)
             else 0
             for x in range(size_x)] for y in range(size_y)]

elif argc > 1 and sys.argv[1] == '4':
    wall = [[1 if (x == wall_x_pos1 and wallTop1 < y < size_y) or (x == wall_x_pos2 and wallTop2 < y < size_y) else 0
             for x in range(size_x)] for y in range(size_y)]

elif argc > 1 and sys.argv[1] == '5':
    wall = [[1 if ((wall_x_pos1 <= x <= wall_x_pos2 and (y == wallTop1 or y == wallTop2)) or (
                wallTop1 >= y >= wallTop2 and x == wall_x_pos2)) else 0
             for x in range(size_x)] for y in range(size_y)]

elif argc > 1 and sys.argv[1] == '6':
    wall = [[1 if ((wall_x_pos1 <= x <= wall_x_pos2 and (y == wallTop1 or y == wallTop2)) or (
                wallTop1 >= y >= wallTop2 and (x == wall_x_pos1 or x == wall_x_pos2))) else 0
             for x in range(size_x)] for y in range(size_y)]

elif argc > 1 and sys.argv[1] == '7':
    wall = [[1 if (2.5 * scale <= x <= 3 * scale and y == 2.5 * scale) or
                  (3 * scale <= x <= 3.5 * scale and y == 2 * scale) or
                  (2.5 * scale >= y >= 2 * scale and x == 3 * scale) or
                  (2 * scale >= y >= 1.5 * scale and x == 3.5 * scale) else 0
             for x in range(size_x)] for y in range(size_y)]
elif argc > 1 and sys.argv[1] == '8':
    wall = [[0 for x in range(size_x)] for y in range(size_y)]