import random

import pygameextra as pe
from pygameextra.mouse import Draggable
from pygameextra.pnzc import PanAndZoomChunks
import time

from game_manager.board_manager import BoardManager

TIME_ANIMATION = 1
TIME_ANIMATION_TEXT = .5


class GameManager:
    pregame_animation_time: float
    pregame_animation_distance: float
    pregame_animation_location: tuple
    gamemode: dict

    pnzc: PanAndZoomChunks

    draggable: pe.mouse.Draggable

    scale_x: float
    scale_y: float

    def __init__(self, data):
        self.data = data
        self.board_manager = BoardManager()

    def start_game(self):
        self.data.state = 'pregame'
        self.pregame_animation_time = time.time()
        self.gamemode = self.data.presets['gamemodes'][
            self.data.ext['gamemode']
        ]
        self.data.save()
        rect = pe.rect.Rect(
            0, 0,
            *[30 * value for value in self.gamemode['grid']]
        )
        self.scale_x = ((self.data.measurements['screen_height'] - 100) / rect.height)
        self.scale_y = ((self.data.measurements['screen_width'] - 100) / rect.width)

        self.scale_x = min(self.scale_x, self.scale_y)
        self.scale_y = self.scale_x
        rect = rect.scale_by(self.scale_x, self.scale_y)
        rect.center = self.data.measurements['screen_half']

        self.draggable = Draggable(rect.topright, rect.size)
        self.draggable.check()

        self.pregame_animation_location = self.data.rects['start_game']['rect'].center

        self.pregame_animation_distance = max(
            *[
                pe.math.dist(
                    self.pregame_animation_location,
                    corner
                ) for corner in (
                    self.draggable.rect.bottomright,
                    self.draggable.rect.bottomleft,
                    self.draggable.rect.topright,
                    self.draggable.rect.topleft
                )]
        )

    def render_animation(self, static=False):
        if static:
            progress = 1.5
        else:
            progress = (time.time() - self.pregame_animation_time) / TIME_ANIMATION
        pregame_animation = int(self.pregame_animation_distance * progress)

        pe.draw.circle((*self.data.ext['color'], 255 * progress),
                       self.pregame_animation_location,
                       pregame_animation + self.data.measurements['outline_width'] * (10 - progress * 10), 0)
        pe.draw.circle(self.data.ext['color'], self.pregame_animation_location, pregame_animation, 0)

        if not static and time.time() > self.pregame_animation_time + TIME_ANIMATION:
            self.data.state = 'start_game'
            self.pregame_animation_time = time.time()
        screen_rect = self.data.measurements['screen_rect']

        top_rect = pe.rect.Rect(screen_rect.left, screen_rect.top, screen_rect.width,
                                self.draggable.rect.top - screen_rect.top)
        bottom_rect = pe.rect.Rect(screen_rect.left, self.draggable.rect.bottom, screen_rect.width,
                                   screen_rect.bottom - self.draggable.rect.bottom)
        left_rect = pe.rect.Rect(screen_rect.left, self.draggable.rect.top, self.draggable.rect.left - screen_rect.left,
                                 self.draggable.rect.height)
        right_rect = pe.rect.Rect(self.draggable.rect.right, self.draggable.rect.top,
                                  screen_rect.right - self.draggable.rect.right,
                                  self.draggable.rect.height)

        pe.draw.rect(self.data.ext['background'], top_rect, 0)
        pe.draw.rect(self.data.ext['background'], bottom_rect, 0)
        pe.draw.rect(self.data.ext['background'], left_rect, 0)
        pe.draw.rect(self.data.ext['background'], right_rect, 0)
        if static:
            self.data.text['beginGameText'].display()
            progress = (time.time() - self.pregame_animation_time) / TIME_ANIMATION_TEXT
            if progress >= 1:
                return
            pe.draw.rect((*self.data.ext['color'], 255 - int(progress * 255)), self.draggable.rect, 0)

    def to_grid_position(self, position):
        grid_size = self.gamemode['grid']
        block_size = self.draggable.rect.width / grid_size[0], self.draggable.rect.height / grid_size[1]
        for x in range(grid_size[0]):
            for y in range(grid_size[1]):
                rect = pe.rect.Rect(
                    block_size[0] * x + self.draggable.rect.left,
                    block_size[1] * y + self.draggable.rect.top,
                    *block_size)
                if rect.collidepoint(position):
                    return x, y
        return 0, 0

    def begin_game(self):
        # TODO: before generating shit, test the math and make zoom and shit
        grid_x, grid_y = self.to_grid_position(pe.mouse.pos())
        self.board_manager.generate_board(*self.gamemode['grid'], *self.gamemode['bombs'], grid_x, grid_y)
        self.data.state = 'in_game'

    def render_game(self):
        pass

    def calculate_lines(self, rect, right_side=False, bottom_side=False, scale=.4):
        sides = [(rect.midtop, (1, 0)), (rect.midleft, (0, 1))]
        if right_side:
            sides.append((rect.midright, (0, 1)))
        if bottom_side:
            sides.append((rect.midbottom, (1, 0)))
        size = rect.height * scale
        lines = [
        ]
        for side, normal in sides:
            lines.append(
                (
                    (
                        side[0] + normal[0] * size,
                        side[1] + normal[1] * size
                    ),
                    (
                        side[0] - normal[0] * size,
                        side[1] - normal[1] * size
                    )
                )
            )
        return lines

    def render_game_lines(self, x, y, w, h, chunk_x, chunk_y):
        rect = pe.rect.Rect(
            x, y, w, h
        )
        lines = self.calculate_lines(
            rect,
            chunk_x == self.gamemode['grid'][0] - 1,
            chunk_y == self.gamemode['grid'][1] - 1,
            scale=.2
        )
        for line in lines:
            pe.draw.line(self.data.ext['color'], *line, 1)

    # def render_chunk(self, chunk, px, py, cx, cy, pnz):
    #     if chunk is None:
    #         return
    #     chunk, chunk_x, chunk_y = chunk
    #     self.render_game_lines(px, py, cx, cy, chunk_x, chunk_y)
