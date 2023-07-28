import pygameextra as pe

from Data import Data
from menu import touch_button


class GamemodeManager:
    def __init__(self, data: Data):
        self.data = data
        self.retheme()

    def render(self, x_center, y_center):
        width = self.data.measurements['play_button_width']
        height = self.data.measurements['play_button_height']
        outline_width = self.data.measurements['outline_width_three_fourths']
        fill_width = width - outline_width
        fill_height = height - outline_width
        rect, gamemode_rect = self.get_rect(self.data.measurements, x_center, y_center, width, height)

        fill_rect = rect.copy()
        fill_rect.width = fill_width
        fill_rect.height = fill_height
        fill_rect.center = rect.center

        fill_rect.center = rect.center

        left_circle_rect = pe.rect.Rect(0, 0, height, height)
        right_circle_rect = left_circle_rect.copy()
        left_gamemode_rect = left_circle_rect.copy()
        right_gamemode_rect = left_circle_rect.copy()
        left_circle_rect.center = rect.midleft
        right_circle_rect.center = rect.midright
        left_gamemode_rect.center = gamemode_rect.midleft
        right_gamemode_rect.center = gamemode_rect.midright
        gamemode_rects = (left_gamemode_rect, right_gamemode_rect)
        circles = (left_circle_rect, right_circle_rect)

        for circle in circles:
            pe.draw.ellipse(
                self.data.ext['color'],
                circle,
                0
            )

        pe.draw.rect(
            self.data.ext['color'],
            rect,
            0
        )
        if not self.is_hovered(rect):
            for circle in circles:
                center = circle.center
                circle.width = fill_height
                circle.height = fill_height
                circle.center = center
                pe.draw.ellipse(
                    self.data.ext['background'],
                    circle,
                    0
                )
            pe.draw.rect(
                self.data.ext['background'],
                fill_rect,
                0
            )
        elif pe.mouse.clicked()[0]:
            self.data.game_manager.start_game()

        touch_button.image(left_gamemode_rect, self.data.surfaces['arrowLeft'],
                           self.data.surfaces['arrowLeftSelected'], self.leftArrow)

        self.data.text['gamemodeText'][self.data.ext['lastGameMode']].display()

        touch_button.image(right_gamemode_rect, self.data.surfaces['arrowRight'],
                           self.data.surfaces['arrowRightSelected'], self.rightArrow)

        return self.is_hovered(rect)

    def retheme(self):
        pass

    @staticmethod
    def is_hovered(rect) -> bool:
        mouse_position = pe.mouse.pos()
        mouse_rect = pe.rect.Rect(*mouse_position, 1, 1)
        return mouse_rect.colliderect(rect)

    @staticmethod
    def get_rect(measurements, x_center, y_center, width, height):
        separation = measurements['outline_width_double']

        rect = pe.rect.Rect(
            x_center - width * .5,
            y_center - height * .5,
            width,
            height
        )

        gamemode_rect = rect.copy()

        gamemode_rect.center = rect.midtop
        gamemode_rect.y -= separation
        rect.center = rect.midbottom
        rect.y += separation
        return rect, gamemode_rect

    def leftArrow(self):
        if self.data.ext['lastGameMode'] > 0:
            self.data.ext['lastGameMode'] -= 1

    def rightArrow(self):
        if self.data.ext['lastGameMode'] < len(self.data.presets['gamemodes']) - 1:
            self.data.ext['lastGameMode'] += 1
