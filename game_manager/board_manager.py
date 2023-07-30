import random


class BoardManager():
    current_board: list
    current_board_map: list
    openings: list
    animation: list

    def __init__(self):
        self.current_board = []
        self.current_board_map = []
        self.openings = []
        self.animation = []

    @staticmethod
    def generate_empty_board(grid_x, grid_y, is_map=False):
        board = []
        for y in range(grid_y):
            layer = []
            for x in range(grid_x):
                if is_map:
                    layer.append('closed')
                else:
                    layer.append('empty')
            board.append(layer)
        return board

    def generate_board(self, grid_x, grid_y, bomb_min, bomb_max, start_x, start_y):
        ok = False
        while not ok:
            self.current_board = self.generate_empty_board(grid_x, grid_y)
            self.current_board_map = self.generate_empty_board(grid_x, grid_y, True)
            protected = [
                (start_x - 1, start_y + 1),
                (start_x, start_y + 1),
                (start_x + 1, start_y + 1),
                (start_x - 1, start_y),
                (start_x, start_y),
                (start_x + 1, start_y),
                (start_x - 1, start_y - 1),
                (start_x, start_y - 1),
                (start_x + 1, start_y - 1),
            ]  # Area around start to be protected
            bombs = random.randint(bomb_min, bomb_max)
            i = 0
            while i < bombs:
                random_x = random.randint(0, grid_x - 1)
                random_y = random.randint(0, grid_y - 1)
                random_location = (random_x, random_y)
                area = [
                    self.current_board[min(max(random_y + 1, 0), grid_y - 1)][min(max(random_x - 1, 0), grid_x - 1)],
                    self.current_board[min(max(random_y + 1, 0), grid_y - 1)][random_x],
                    self.current_board[min(max(random_y + 1, 0), grid_y - 1)][min(max(random_x + 1, 0), grid_x - 1)],
                    self.current_board[random_y][min(max(random_x - 1, 0), grid_x - 1)],
                    self.current_board[random_y][min(max(random_x + 1, 0), grid_x - 1)],
                    self.current_board[min(max(random_y - 1, 0), grid_y - 1)][min(max(random_x - 1, 0), grid_x - 1)],
                    self.current_board[min(max(random_y - 1, 0), grid_y - 1)][random_x],
                    self.current_board[min(max(random_y - 1, 0), grid_y - 1)][min(max(random_x + 1, 0), grid_x - 1)],
                ]
                if (random_location in protected) or (self.current_board[random_y][random_x] == 'bomb') or (not ('empty' in area)):
                    continue
                self.current_board[random_y][random_x] = 'bomb'
                i += 1
            visited = []
            unvisited = {(start_x, start_y)}
            while unvisited:
                current = unvisited.pop()
                visited.append(current)
                for neighbour in self.neighbouring_squares(current, grid_x, grid_y):
                    if self.current_board[neighbour[1]][neighbour[0]] == "empty":
                        if neighbour not in visited:
                            unvisited.add(neighbour)
            if len(visited) + bombs == grid_x * grid_y:
                ok = True
                # Generate map
                self.uncover(start_x, start_y, grid_x, grid_y)
        return self.current_board, self.current_board_map

    @staticmethod
    def neighbouring_squares(center, grid_x, grid_y, filter_by=None, board=None):
        random_x = center[0]
        random_y = center[1]
        area = [
            (random_y + 1, random_x - 1),
            (random_y + 1, random_x),
            (random_y + 1, random_x + 1),
            (random_y, random_x - 1),
            (random_y, random_x + 1),
            (random_y - 1, random_x - 1),
            (random_y - 1, random_x),
            (random_y - 1, random_x + 1)]
        i = 0
        while i < len(area):
            area[i] = (area[i][1], area[i][0])
            if area[i][0] < 0 or area[i][0] > grid_x - 1:
                del area[i]
            elif area[i][1] < 0 or area[i][1] > grid_y - 1:
                del area[i]
            elif filter_by is not None and board is not None and board[area[i][1]][area[i][0]] != filter_by:
                del area[i]
            else:
                i += 1
        return area

    def uncover(self, start_x, start_y, grid_x, grid_y):
        visited = []
        unvisited = {(start_x, start_y)}
        size_of_opening = 30
        uncovered = 0
        while unvisited:
            current = unvisited.pop()
            visited.append(current)
            self.openings.append([current, size_of_opening])
            self.animation.append({
                'type': 'opening',
                'location': current
            })
            uncovered += 1
            size_of_opening += 1
            surround = 0
            empty = []
            for neighbour in self.neighbouring_squares(current, grid_x, grid_y):
                if neighbour not in visited:
                    if self.current_board[neighbour[1]][neighbour[0]] == 'bomb':
                        surround += 1
                    elif self.current_board_map[neighbour[1]][neighbour[0]] == 'closed':
                        empty.append(neighbour)
            if surround == 0:
                self.current_board_map[current[1]][current[0]] = 'opened'
                unvisited.update(empty)
            else:
                self.current_board_map[current[1]][current[0]] = str(surround)
        return uncovered
