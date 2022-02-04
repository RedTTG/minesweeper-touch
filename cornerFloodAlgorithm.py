from Grid import Grid
from time import time
def filtered(grid:(Grid, list), filter, toCheck:list=[], recursionLimit=1000):
    formatOfGrid = 'normal'

    if type(grid) is list:
        grid = Grid(grid)
        formatOfGrid = 'old'

    result = Grid(sizeX=grid.sizeX, sizeY=grid.sizeY)

    if len(toCheck) < 1:
        for x, y in grid.allPositions:
            if grid.getAt(x, y) == filter:
                toCheck.append((x, y))
    recursion = 0
    while recursion < recursionLimit and len(toCheck) > 0:
        visited = []
        unvisited = {(toCheck[0])}
        while unvisited:
            current = unvisited.pop()
            if current in toCheck:
                del toCheck[toCheck.index(current)]
            visited.append(current)
            sides = []
            for neighbour in grid.neighbouringSquares(current):
                if neighbour:
                    if grid.getAt(*neighbour) == filter:
                        if neighbour not in visited:
                            unvisited.add(neighbour)
                            recursion += 1
                        sides.append(False)
                    else:
                        sides.append(True)
                else:
                    sides.append(False)
            sides2 = []
            if sides[6] and sides[7] and sides[3]:
                sides2.append(True)
            else:
                sides2.append(False)
            if sides[8] and sides[7] and sides[5]:
                sides2.append(True)
            else:
                sides2.append(False)
            if sides[0] and sides[1] and sides[3]:
                sides2.append(True)
            else:
                sides2.append(False)
            if sides[2] and sides[1] and sides[5]:
                sides2.append(True)
            else:
                sides2.append(False)
            result.setAt(*current, sides2)
    result.replaceAll(None, [False]*4)
    if formatOfGrid == 'normal':
        return result
    else:
        return result.grid