def generateEmptyGrid(gridX, gridY, value):
    board = []
    for y in range(gridY):
        layer = []
        for x in range(gridX):
            layer.append(value)
        board.append(layer)
    return board

class Grid:
    def __init__(self, grid = None, sizeX=None, sizeY=None):
        if grid is None:
            if sizeX is None:
                sizeX = 5
            if sizeY is None:
                sizeY = 5
            grid = generateEmptyGrid(sizeX, sizeY, None)
        self.grid = grid
        if sizeX is None:
            if len(grid)>0:
                sizeX = len(grid[0])
            else:
                sizeX = 0
        if sizeY is None:
            sizeY = len(grid)
        self.sizeX = sizeX
        self.sizeY = sizeY
        x = 0
        y = 0
        positions = []
        while y < self.sizeY:
            while x < self.sizeX:
                positions.append((x, y))
                x += 1
            y += 1
            x = 0
        self.allPositions = positions
    def getAt(self, x, y):
        return self.grid[y][x]
    def setAt(self, x, y, value):
        self.grid[y][x] = value
    def neighbouringSquares(self, center):
        randomX = center[0]
        randomY = center[1]
        area = [(randomY + 1, randomX - 1), (randomY + 1, randomX), (randomY + 1, randomX + 1), (randomY, randomX - 1),None, (randomY, randomX + 1), (randomY - 1, randomX - 1), (randomY - 1, randomX),(randomY - 1, randomX + 1)]
        i = 0
        while i < len(area):
            if not area[i]:
                i += 1
                continue
            area[i] = (area[i][1], area[i][0])
            if area[i][0] < 0 or area[i][0] > self.sizeX - 1:
                area[i] = None
            elif area[i][1] < 0 or area[i][1] > self.sizeY - 1:
                area[i] = None
            i += 1
        return area
    def replaceAll(self, fromV, toV):
        x, y = 0, 0
        for yi in self.grid:
            for xi in yi:
                if xi == fromV:
                    self.grid[y][x] = toV
                x += 1
            x = 0
            y += 1