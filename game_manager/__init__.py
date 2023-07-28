import pygameextra as pe
import time

TIME_ANIMATION = 1
TIME_ANIMATION_TEXT = .5


class GameManager:
    pregame_animation_time: float
    pregame_animation_distance: float
    gamemode: int

    rect: pe.rect.Rect

    scalex: float
    scaley: float

    def __init__(self, data):
        self.data = data

    def start_game(self):
        self.data.state = 'pregame'
        self.pregame_animation_time = time.time()
        gamemode = self.data.presets['gamemodes'][
            self.data.ext['lastGameMode']
        ]
        self.data.save()
        self.rect = pe.rect.Rect(
            0, 0,
            *[30 * value for value in gamemode['grid']]
        )
        self.scalex = ((self.data.measurements['screen_height'] - 100) / self.rect.height)
        self.scaley = ((self.data.measurements['screen_width'] - 100) / self.rect.width)

        self.scalex = min(self.scalex, self.scaley)
        self.scaley = self.scalex

        self.rect = self.rect.scale_by(self.scalex, self.scaley)

        self.rect.center = self.data.measurements['screen_half']


        self.pregame_animation_distance = pe.math.dist(
            self.rect.center,
            self.rect.bottomright
        )

    def render_animation(self, static=False):
        if static:
            progress = 1.5
        else:
            progress = (time.time() - self.pregame_animation_time) / TIME_ANIMATION
        pregame_animation = int(self.pregame_animation_distance * progress)
        pe.draw.circle((*self.data.ext['color'], 255*progress),
                       self.data.measurements['screen_half'],
                       pregame_animation + self.data.measurements['outline_width']*(10-progress*10), 0)
        pe.draw.circle(self.data.ext['color'], self.data.measurements['screen_half'], pregame_animation, 0)
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
            pe.draw.rect((*self.data.ext['color'], 255-int(progress*255)), self.rect, 0)

    def begin_game(self):
        # TODO: before generating shit, test the math and make zoom and shit
        # generateBoard(*self.gamemode['grid'], *self.gamemode['bombs'], gridX, gridY)
        pass