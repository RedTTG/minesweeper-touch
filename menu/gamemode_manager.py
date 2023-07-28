import pygameextra as pe

from Data import Data


class GamemodeManager:
    def __init__(self, data: Data):
        self.data = data
        self.retheme()

    def render(self, x_center, y_center):
        width = self.data.measurements['play_button_width']
        height = self.data.measurements['play_button_height']
        outline_width = self.data.measurements['outline_width_three_fourths']
        separation = self.data.measurements['outline_width_double']
        fill_width = width - outline_width
        fill_height = height - outline_width
        rect = self.get_rect(x_center, y_center, width, height)

        gamemode_rect = rect.copy()

        gamemode_rect.center = rect.midtop
        gamemode_rect.y -= separation
        rect.center = rect.midbottom
        rect.y += separation

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
            if pe.mouse.clicked()[0]:
                self.data.game_manager.start_game()

        for gamemode_rect in gamemode_rects:
            pe.draw.rect(
                self.data.ext['color'],
                gamemode_rect,
                0
            )
            if not self.is_hovered(rect):
                pe.draw.rect(
                    self.data.ext['color'],
                    gamemode_rect,
                    0
                )

        # if self.is_hovered(rect):

    def retheme(self):
        pass

    @staticmethod
    def is_hovered(rect) -> bool:
        mouse_position = pe.mouse.pos()
        mouse_rect = pe.rect.Rect(*mouse_position, 1, 1)
        return mouse_rect.colliderect(rect)

    def get_rect(self, x_center, y_center, width, height):
        return pe.rect.Rect(
            x_center - width * .5,
            y_center - height * .5,
            width,
            height
        )
