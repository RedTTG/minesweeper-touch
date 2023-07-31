import random

import pygameextra as pe
from pygameextra.mouse import Draggable
from pygameextra.pnzc import PanAndZoomChunks
import time

from game_manager.board_manager import BoardManager
from game_manager.render_spiral import render_spiral

TIME_ANIMATION = 1
TIME_ANIMATION_TEXT = .5


class GameManager:
    pregame_animation_time: float
    pregame_animation_distance: float
    pregame_animation_location: tuple
    gamemode: dict

    draggable: pe.mouse.Draggable
    rect: pe.rect.Rect

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
        self.rect = pe.rect.Rect(
            0, 0,
            *[30 * value for value in self.gamemode['grid']]
        )
        self.scale_x = ((self.data.measurements['screen_height'] - 100) / self.rect.height)
        self.scale_y = ((self.data.measurements['screen_width'] - 100) / self.rect.width)

        self.scale_x = min(self.scale_x, self.scale_y)
        self.scale_y = self.scale_x
        self.rect = self.rect.scale_by(self.scale_x, self.scale_y)
        self.rect.center = self.data.measurements['screen_half']

        self.draggable = Draggable(self.rect.topleft)
        self.draggable.check()

        self.pregame_animation_location = self.data.rects['start_game']['rect'].center

        self.pregame_animation_distance = max(
            *[
                pe.math.dist(
                    self.pregame_animation_location,
                    corner
                ) for corner in (
                    self.rect.bottomright,
                    self.rect.bottomleft,
                    self.rect.topright,
                    self.rect.topleft
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
                                self.rect.top - screen_rect.top)
        bottom_rect = pe.rect.Rect(screen_rect.left, self.rect.bottom, screen_rect.width,
                                   screen_rect.bottom - self.rect.bottom)
        left_rect = pe.rect.Rect(screen_rect.left, self.rect.top, self.rect.left - screen_rect.left,
                                 self.rect.height)
        right_rect = pe.rect.Rect(self.rect.right, self.rect.top,
                                  screen_rect.right - self.rect.right,
                                  self.rect.height)

        pe.draw.rect(self.data.ext['background'], top_rect, 0)
        pe.draw.rect(self.data.ext['background'], bottom_rect, 0)
        pe.draw.rect(self.data.ext['background'], left_rect, 0)
        pe.draw.rect(self.data.ext['background'], right_rect, 0)
        if static:
            self.data.text['beginGameText'].display()
            progress = (time.time() - self.pregame_animation_time) / TIME_ANIMATION_TEXT
            if progress >= 1:
                return
            pe.draw.rect((*self.data.ext['color'], 255 - int(progress * 255)), self.rect, 0)

    def to_grid_position(self, position):
        grid_size = self.gamemode['grid']
        block_size = self.rect.width / grid_size[0], self.rect.height / grid_size[1]
        for x in range(grid_size[0]):
            for y in range(grid_size[1]):
                rect = pe.rect.Rect(
                    block_size[0] * x + self.rect.left,
                    block_size[1] * y + self.rect.top,
                    *block_size)
                if self.data.DEBUG:
                    pe.draw.rect(pe.colors.red, rect, 1)
                if rect.collidepoint(position):
                    return x, y
        return 0, 0

    def begin_game(self):
        # TODO: before generating shit, test the math and make zoom and shit
        grid_x, grid_y = self.to_grid_position(pe.mouse.pos())
        self.board_manager.generate_board(*self.gamemode['grid'], *self.gamemode['bombs'], grid_x, grid_y)
        self.data.state = 'in_game'

    def render_game(self):
        grid_size = self.gamemode['grid']
        block_size = self.rect.width / grid_size[0], self.rect.height / grid_size[1]
        screen_size = self.data.measurements['screen']
        moving, pos = self.draggable.check()
        self.rect.topleft = pos
        if self.data.DEBUG:
            if moving:
                pe.draw.rect(pe.colors.blue, self.rect, 2)
            else:
                pe.draw.rect(pe.colors.yellow, self.rect, 1)

        visible_rect = self.rect.clip(pe.rect.Rect(0, 0, screen_size[0], screen_size[1]))

        if self.data.DEBUG:
            pe.draw.rect(pe.colors.darkpink, visible_rect, 1)

        # If the visible rect has a valid width and height (i.e., not entirely off-screen)
        if visible_rect.width > 0 and visible_rect.height > 0:
            start_chunk_x = max(0, int((visible_rect.left - self.rect.left) / block_size[0]))
            start_chunk_y = max(0, int((visible_rect.top - self.rect.top) / block_size[1]))

            # Calculate the cell indices of the top-left and bottom-right corners of the visible rect
            end_chunk_x = min(grid_size[0], start_chunk_x + int(visible_rect.width / block_size[0]) + 1)
            end_chunk_y = min(grid_size[1], start_chunk_y + int(visible_rect.height / block_size[1]) + 1)

            
            for x, y in render_spiral(start_chunk_x, start_chunk_y, end_chunk_x, end_chunk_y, 500):
                self.render_chunk(x, y, block_size, grid_size)

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

    def render_game_lines(self, x, y, w, h, chunk_x, chunk_y, grid_size):
        rect = pe.rect.Rect(
            x, y, w, h
        )
        lines = self.calculate_lines(
            rect,
            chunk_x == grid_size[0] - 1,
            chunk_y == grid_size[1] - 1,
            scale=.2
        )
        for line in lines:
            pe.draw.line(self.data.ext['color'], *line, 1)

    def render_chunk(self, chunk_x, chunk_y, block_size, grid_size):
        x, y = self.rect.left + chunk_x * block_size[0], self.rect.top + chunk_y * block_size[1]
        self.render_game_lines(x, y, *block_size, chunk_x, chunk_y, grid_size)

    # def render_color(self, chunk_x, chunk_y, block_size, grid_size):
    #     x, y = self.rect.left + chunk_x * block_size[0], self.rect.top + chunk_y * block_size[1]
    #     rect = pe.rect.Rect(x, y, *block_size)
    #     pe.draw.rect(self.data.ext['color'], rect, 0)
