import random

import pygameextra as pe
import time

from game_manager.board_manager import BoardManager

TIME_ANIMATION = 1
TIME_ANIMATION_TEXT = .5


class GameManager:
    pregame_animation_time: float
    pregame_animation_distance: float
    gamemode: dict

    rect: pe.rect.Rect

    scalex: float
    scaley: float

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
        self.scalex = ((self.data.measurements['screen_height'] - 100) / self.rect.height)
        self.scaley = ((self.data.measurements['screen_width'] - 100) / self.rect.width)

        self.scalex = min(self.scalex, self.scaley)
        self.scaley = self.scalex

        self.rect = self.rect.scale_by(self.scalex, self.scaley)

        self.rect.center = self.data.measurements['screen_half']

        self.pregame_animation_location = self.data.rects['start_game']['rect'].center

        self.pregame_animation_distance = max(*[
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
            self.data.state = 'startgame'
            self.pregame_animation_time = time.time()
        screen_rect = self.data.measurements['screen_rect']

        top_rect = pe.rect.Rect(screen_rect.left, screen_rect.top, screen_rect.width, self.rect.top - screen_rect.top)
        bottom_rect = pe.rect.Rect(screen_rect.left, self.rect.bottom, screen_rect.width,
                                   screen_rect.bottom - self.rect.bottom)
        left_rect = pe.rect.Rect(screen_rect.left, self.rect.top, self.rect.left - screen_rect.left,
                                 self.rect.height)
        right_rect = pe.rect.Rect(self.rect.right, self.rect.top, screen_rect.right - self.rect.right,
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
                if rect.collidepoint(position):
                    return x, y
        return 0, 0

    def begin_game(self):
        # TODO: before generating shit, test the math and make zoom and shit
        grid_x, grid_y = self.to_grid_position(pe.mouse.pos())
        self.board_manager.generate_board(*self.gamemode['grid'], *self.gamemode['bombs'], grid_x, grid_y)
        self.data.state = 'ingame'
