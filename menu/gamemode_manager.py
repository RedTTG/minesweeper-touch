import pygameextra as pe

from Data import Data
from menu import touch_button


class GamemodeManager:
    def __init__(self, data: Data):
        self.data = data
        self.retheme()

    def render(self, suffix=''):
        start_game_rect_dict = self.data.rects[f'start_game{suffix}']
        gamemode_rect_dict = self.data.rects[f'gamemode{suffix}']

        width = self.data.measurements['play_button_width']
        height = self.data.measurements['play_button_height']
        outline_width = self.data.measurements['outline_width_three_fourths']
        fill_width = width - outline_width
        fill_height = height - outline_width
        rect, gamemode_rect, left_gamemode_rect, right_gamemode_rect = start_game_rect_dict['rect'], gamemode_rect_dict[
            'rect'], gamemode_rect_dict['left'], gamemode_rect_dict['right']

        fill_rect = rect.copy()
        fill_rect.width = fill_width
        fill_rect.height = fill_height
        fill_rect.center = rect.center

        fill_rect.center = rect.center

        left_circle_rect = pe.rect.Rect(0, 0, height, height)
        right_circle_rect = left_circle_rect.copy()
        left_circle_rect.center = rect.midleft
        right_circle_rect.center = rect.midright
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
        if not (is_hovered := self.is_hovered(rect)):
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
            self.data.text[f'start_game{suffix}'].display()
        elif pe.mouse.clicked()[0]:
            self.data.game_manager.start_game()

        for side in ['left', 'right']:
            touch_button.image(
                gamemode_rect_dict[side],
                self.data.surfaces[f'{side}_gamemode{suffix}'],
                self.data.surfaces[f'{side}_gamemode_selected{suffix}'],
                self.leftArrow if side == 'left' else self.rightArrow
            )

        self.data.text[f'gamemode{suffix}'][self.data.ext['gamemode']].display()
        if is_hovered:
            self.data.text[f'start_game_selected{suffix}'].display()

    def retheme(self):
        pass

    @staticmethod
    def is_hovered(rect) -> bool:
        mouse_position = pe.mouse.pos()
        return rect.collidepoint(mouse_position)

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

        block_size = [measurements['block_size']] * 2

        left_gamemode_rect = pe.rect.Rect(0, 0, *block_size)
        right_gamemode_rect = left_gamemode_rect.copy()
        left_gamemode_rect.center = gamemode_rect.midleft
        right_gamemode_rect.center = gamemode_rect.midright
        left_gamemode_rect.x += measurements['outline_width_double']
        right_gamemode_rect.x -= measurements['outline_width_double']

        return rect, gamemode_rect, left_gamemode_rect, right_gamemode_rect

    def leftArrow(self):
        if self.data.ext['gamemode'] > 0:
            self.data.ext['gamemode'] -= 1

    def rightArrow(self):
        if self.data.ext['gamemode'] < len(self.data.presets['gamemodes']) - 1:
            self.data.ext['gamemode'] += 1
